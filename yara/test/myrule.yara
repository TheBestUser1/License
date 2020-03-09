rule myrule
{
	meta:
	     author="TheBestUser"
	     date="01/03/2020"
             description="This is a test"

	strings:
	     $s1="VirtualAlloc"
	     $h1={ 68 54 CA AF 91 }	
	
	condition:
	     $s1 or $h1
}
