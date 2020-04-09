#include<iostream>
#include<windows.h>

typedef LPVOID* (*_func)(void*, void*, char*, void*);

int main(int argc, char**argv) {

	HANDLE bytes = CreateFileA(argv[1], GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	DWORD size = GetFileSize(bytes, NULL);
	DWORD read;
	CHAR* BUFF = new CHAR[size];
	int ok = ReadFile(bytes, BUFF, size, &read, 0);

	HANDLE bytes_d = CreateFileA(argv[2], GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	DWORD size2 = GetFileSize(bytes_d,NULL);
	CHAR * BUFF2 = new CHAR[size2];
	DWORD read_d;
	int ok2 = ReadFile(bytes_d, BUFF2, size2, &read_d, 0);

	LPVOID addr_exec = VirtualAlloc(NULL, size, MEM_COMMIT,PAGE_EXECUTE_READWRITE);

	memcpy(addr_exec, BUFF, read);

	_func run = (_func)addr_exec;
	char file[] = "ceva";
	run((void*)((CHAR*)BUFF2),(DWORD*)size,file,(char*)'r');

	return 0;
}
