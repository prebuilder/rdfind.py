__all__ = ("DupType", "Dupe", "findDuplicates", "parseDupesFile", "dedup")
import csv
import fcntl
import os
import typing
from enum import Enum
from pathlib import Path

import sh


class rdfindDialect(csv.Dialect):
	delimiter = " "
	skipinitialspace = False
	lineterminator = "\n"
	quoting = csv.QUOTE_NONE


class DupType(Enum):
	unknown = "DUPTYPE_UNKNOWN"
	firstOccurrence = "DUPTYPE_FIRST_OCCURRENCE"
	withinSameTree = "DUPTYPE_WITHIN_SAME_TREE"
	outsideTree = "DUPTYPE_OUTSIDE_TREE"


class Dupe:
	__slots__ = ("type", "identity", "depth", "size", "device", "inode", "cmdlineIndex", "path")

	def __init__(self, dic: typing.Mapping):
		for k, v in dic.items():
			setattr(self, k, v)

	def toDict(self):
		return {k: getattr(self, k) for k in __class__.__slots__}

	def __repr__(self):
		return self.__class__.__name__ + "(" + repr(self.toDict()) + ")"


currentProcFileDescriptors = Path("/proc") / str(os.getpid()) / "fd"


def parseDupesFile(dupesLines: typing.Iterable[str]) -> typing.Iterable[Dupe]:
	for r in csv.DictReader((l for l in dupesLines if l[0] != "#"), fieldnames=Dupe.__slots__, dialect=rdfindDialect):
		r["type"] = DupType(r["type"])
		r["identity"] = int(r["identity"])
		r["depth"] = int(r["depth"])
		r["size"] = int(r["size"])
		r["device"] = int(r["device"])
		r["inode"] = int(r["inode"])
		r["cmdlineIndex"] = int(r["cmdlineIndex"])
		r["path"] = Path(r["path"])
		yield Dupe(r)


def findDuplicates_(*dirsToDedup: typing.Iterable[Path]) -> str:
	"""Invokes `rdfind` and returns dupes as `Dupe` objects"""
	dirsToDedup = [Path(p).absolute() for p in dirsToDedup]
	pO, pI = os.pipe()
	try:
		fcntl.fcntl(pO, fcntl.F_SETFL, os.O_NONBLOCK)
		with os.fdopen(pO, "rb") as pOF:
			res = []
			sp = sh.rdfind.bake(deterministic="true", outputname=str(currentProcFileDescriptors / str(pI)), checksum="sha256", _long_prefix="-", _long_sep=" ", _bg=True)(*dirsToDedup)

			while sp.process.is_alive()[0]:
				chunk = pOF.read()
				if chunk:
					res.append(chunk)

			return b"".join(res).decode("utf-8")

	finally:
		os.close(pI)
		try:
			os.close(pO)
		except:
			pass


def findDuplicates(*dirsToDedup: typing.Iterable[Path]) -> typing.Iterable[Dupe]:
	return parseDupesFile(findDuplicates_(*dirsToDedup).splitlines())


def relPath(src, dst):
	src = Path(src).absolute()
	dst = Path(dst).absolute()
	commonPath = Path(os.path.commonpath((src, dst)))
	cpl = len(commonPath.parts)
	up = (".." + os.sep) * (len(dst.parts) - cpl)
	down = os.sep.join(src.parts[cpl - len(src.parts) :])
	return Path(up) / down


def dedup(dir: Path, relativeTo: typing.Optional[Path] = None, relativePath: bool = True):
	"""Replaces dupes with symlinks to them."""
	dir = Path(dir).absolute()
	if relativeTo is not None:
		relativeFd = os.open(relativeTo, os.O_RDONLY)

		def symlinkerFunc(src, dst):
			return os.symlink(src.relative_to(relativeTo), dst, dir_fd=relativeFd)

	else:
		relativeFd = None
		symlinkerFunc = os.symlink

	try:
		dupes = findDuplicates(dir)
		stor = {}
		for d in dupes:
			i = d.identity
			if i < 0:
				i = -i
				orig = stor[i]
				src = orig.path
				dst = d.path
				dst.unlink()
				if relativePath:
					try:
						dstP = dst.parent
						relP = relPath(src, dstP)
						dstPFd = os.open(dstP, os.O_RDONLY)
						try:
							os.symlink(relP, dst, dir_fd=dstPFd)
						except Exception as ex:
							raise
						finally:
							os.close(dstPFd)
					except Exception as ex:
						symlinkerFunc(src, dst)
				else:
					symlinkerFunc(src, dst)
			else:
				stor[i] = d
	except Exception as ex:
		raise
	finally:
		if relativeFd is not None:
			os.close(relativeFd)
