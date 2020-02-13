
def handle_uploaded_file(x):
  breakpoint()
  with open(x,"wb+")as destination:
        for chunk in f.chunks():
            destination.write(chunk)
