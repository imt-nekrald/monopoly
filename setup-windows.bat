call mkdir C:\local
call cd /D C:\local
call git clone https://github.com/microsoft/vcpkg.git
call cd vcpkg
call bootstrap-vcpkg.bat
call vcpkg install libxlsxwriter:x64-windows
call vcpkg install jsoncpp
call vcpkg integrate install

