#include<iostream>
#include<windows.h>

typedef LPVOID* (*_func)(void*, void*, void*, void*);

int main(int argc, char**argv) {

	HANDLE bytes = CreateFileA(argv[1], GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	DWORD size = GetFileSize(bytes, NULL);
	DWORD read;
	CHAR* BUFF = new CHAR[size];
	int ok = ReadFile(bytes, BUFF, size, &read, 0);
  HANDLE bytes2 = CreateFileA(argv[2],GENERIC_READ,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL);
  DWORD size2 = GetFileSize(bytes2,NULL);
  CHAR* Crypted = new CHAR[size2];


	LPVOID addr_exec = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

	memcpy(addr_exec, BUFF, read);
	_func run = (_func)addr_exec;
  std::cout<<"Here we got and we are fine"<<std::endl;
  run(NULL,NULL,NULL,NULL);

	return 0;
}
