# Python ZWO EAF Python bindings

These are Python bindings for the manufacturer-provided C++ drivers for one specific model of Electronic Auto Focuser for an astronomy telescope.

Tested on this product: https://astronomy-imaging-camera.com/product/eaf-5v/
on Arch Linux x86-64. No plans to include support for more platforms. Original C++ drivers are from here: https://www.zwoastro.com/software/

Requires libudev installed to work.

For those who don't know how c extensions work:

Python can import modules from a C shared object file (`.so`) that's built from a source file that uses some special constructs provided by `Python.h` to define a module and expose functions. Cython will take a `.pxd` and `.pyx` file that have their own special syntax, and generate that C file for you, then compile it to a `.so` file that Python can import. Since those files are in C, they can use the library function we want as long as we include the header and link the library's `.so`. We use `setup.py` to do the build in a way that correctly links to the dependency libraries.

When I was trying to figure all this out, this video helped a lot to understand on the lowest level what is going on with importing C code into Python: https://www.youtube.com/watch?v=nHEF1epuuco&pp=ygUTcHl0aG9uICBjIGV4dGVuc2lvbg%3D%3D

I couldn't be bothered to make real docs but the available interface is roughly as follows:

```python
def getNumEAFs() # number of EAFs plugged in
def getEAFID(int index) # get ID of an EAF that's plugged in (first one is index 0)


class EAF:
    def get_max_step(self) # max position EAF can go to

    def move_to(step: int):

    def stop():

    def get_moving_status():
        '''
        Returns the moving status of the focuser.
        The 3 states are NOT_MOVING, MOVING, and MOVING_WITH_HANDLE.
        NOT_MOVING: The focuser is not moving.
        MOVING: The focuser is moving, but it can be stopped by the `stop()` method.
        MOVING_WITH_HANDLE: The focuser is moving, and it cannot be stopped by the `stop()` method.
        '''
    
    def is_moving():
        '''
        Returns True if the focuser is moving, False otherwise.

        This thing is inconsistent as hell. It's better to just check if
        the position is changing, or if it's reached the target position and then
        call `stop()`.
        '''

    def get_position():

```