from pyhdmap.api.hdmap import PyHDMap, Mode

if __name__ == "__main__":
  pyhdmap = PyHDMap()
  pyhdmap.set_mode(Mode.REMOTE)
  hdmap = pyhdmap.get_manager()