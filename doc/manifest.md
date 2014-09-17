# XD-embedded manifest

A manifest consists of a stack of layers.

There are different layer types:

1. Metadata layers
2. Python library layers


## Metadata layers

Metadata layers must be placed in a subdirectory of the meta/ subdirectory of
the XD-embedded manifest (except for the manifest layer, which is simply the
manifest top-level directory).  The subdirectory must be have the same name as
the layer.  The XD-build core metadata layer must fx. be placed in the
meta/core subdirectory of the manifest.

Metadata layers can provide

1. XD-build recipes.  An XD-build recipe is a specification of how to build a
   specific software package.  XD-build recipes must be placed in the recipes/
   subdirectory of the layer, and must have file extension '.xd'.

2. XD-build classes.  Specification of common rules for building software
   packages, fx. common rules for building packages using the cmake build
   system.  XD-build classes must be placed in the classes/ subdirectory of the
   layer, and must have file extension '.xdc.'

3. XD-embedded Python modules.  Python library code for use by fx. XD-build
   classes and recipes.  XD-embedded Python modules must be placed in the lib/
   subdirectory of the layer, and must have the file extension '.py'.  Such
   modules will be included in the xd.meta namespace, so that
   fx. meta/core/lib/foo will be available as xd.meta.core.foo in Python.
   XD-embedded Python modules in manifest layer are available as
   xd.meta.manifest in Python.

4. XD-embedded commands.  Additional commands available through the XD-tool
   command.  The 'xd build' command is fx. provided by the XD-build core
   metadata layer.  Commands are a special case of Python modules, contained
   in the cmd package of the XD-embedded Python modules subdirectory of the
   layer.  So the 'xd build' command is fx. implemented in lib/cmd/build.py of
   the XD-build core metadata layer (ie. meta/core/lib/cmd/build.py in the
   manifest).

While the XD-build core metadata layer will provide all 4 of the above
mentioned, other layers might provide only some of it.  Many layers might just
provide recipes, and others just recipes and classes.


## Python library layers

Python library layers are a way of integrating external Python libraries into
an XD-embedded manifest.  Hopefully, this will not be needed a lot.  An example
could be the urlgrabber library, which could be included in the manifest by
placing it in lib/urlgrabber of the manifest.


## Setting up the stack

How do we setup the stack?

Preferably, we should be able to set it up without having to do anything.

This might be possible if all layers are setup with either unique priorities,
or enough layer dependencies to setup a unique order.  By maintaining a global
layer index, listing all available layers, and which layer(s) they come
before, and/or which layers they come after, this information should be kept
in a configuration file in the layer, and XD-tool will retrieve this
information, and build up a list of layers in order.

Alternatively, it must also be possible to specify a specific (non-standard)
stack order in a configuration file in the manifest.  This could fx. be
necessary if some layers have wrong priority information, or the manifest
maintainer for some odd reason needs to use a non-standard layer order.

The result of XD-tool setting this up should be in the form of XD_METAPATH and
XD_PYTHONPATH variables.

The XD_PYTHONPATH variable is in the same form as the standard PYTHONPATH, and
will be prepended to sys.path.  Actually, the XD_PYTHONPATH is not really
needed afterwards, but it needs to be included in the metadata for signature
calculations.

The XD_METAPATH variable is a comma separated list of directory paths
(relative to XD_TOPDIR).  It should be in this form (instead of a real Python
list), so that it is handled in the same way as if it was specified by a shell
environment variable.


## Probing manifest for XD-embedded commands

After XD-tool has figured out the correct XD_METAPATH, it can go through all
layers in order, and add all commands found.


## Finding manifest

Recurse up the directory structure, until git repository with a '.xd' file in
the base directory is found.
