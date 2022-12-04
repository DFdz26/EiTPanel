import fakeConnectionSAP

ident = "4465441"
lines = fakeConnectionSAP.search_item(ident, fakeConnectionSAP.DB_NAME)
print(f'The product with identification {ident}, belong to the assembly line {lines}')

print(f'*****************************************')
ident = "9320058"
print(f'Maybe the same product can belong to different assembly lines and the person should decide where it should go:')
lines = fakeConnectionSAP.search_item(ident, fakeConnectionSAP.DB_NAME)
print(f'The product with identification {ident}, belong to the assembly lines {lines}')
print(f'Or this can be automatized if a assembly line requires the piece so, inside of the options we select the '
      f'one that required the piece.')
