# conan-cgcc
Conan recipe to create a cross-compiler for arm64

---

## Dependencies
* [Conan](https://conan.io/) >= 1.0.0 
    * Conan need Python. Conan is compatible with Python 2 and Python 3 
    * Recommended is the Installation with pip
        ```bash
        pip install conan
        ```

* gcc >=  5.4
    * Linux: gcc is installed by default on Ubuntu 16.04
* g++ >=  5.4
    * Linux: g++ is installed by default on Ubuntu 16.04
* gfortran >= 5.4
    * Linux: gfortran is not installed by default on Ubuntu 16.04 
* make >=4.1
    * Linux: make is not installed by default on Ubuntu 16.04  
* gawk
    ```bash
        sudo apt-get install gawk
    ```
* Recommended (and tested with Ubuntu 16.04)
## Basic Build Instructions

1. Clone this repo.
2. Run 
    ```bash
        conan create . [user]/[channel] -s arch=armv8
    ```
3. Change to your project folder
4. Add this lines to your new/existing conanfile 
    ```python
        def build_requirements(self):
            if self.settings.arch == "armv8":
                self.build_requires("CrossGccConan/5.4.0@[user]/[channel]")
    ```
5. Run
    ```bash
        conan create . [user]/[channel] -s arch=armv8
    ```
