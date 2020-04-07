#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/mman.h>


typedef void (*_function)();






int main()
{
  FILE *p = fopen("f_dumpde","rb");
  fseek(p,0,SEEK_END);
  int size = ftell(p);
  rewind(p);
  int fd = fileno(p);
  /*printf("%d",size);
  void* function;
  function = malloc(size);
  fread((unsigned char*)((void*)function),size,1,p);*/
  void *test = mmap(0,size,PROT_EXEC|PROT_READ,MAP_PRIVATE,fd,0);
  //memcpy(test,function,size);
  printf("it's working till here\n");
  _function a = (_function)test;
  a();

  return 0;


}
