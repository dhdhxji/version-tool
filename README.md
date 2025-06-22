## Version tools
Tools for embedding version information into the software with cmake support, keeping track of the git changes in a build-system agnostic way

## Example
The top-level dir contains a simplistic example, which just prints out the version.
To build it, use the cmake:

```shell
mkdir build
cd build
cmake ..
make
./app
```

