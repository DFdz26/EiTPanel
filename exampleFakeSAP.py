import fakeConnectionSAP

lines = fakeConnectionSAP.search_item(8721, fakeConnectionSAP.DB_NAME)
print(f'The product with identification 8721, belong to the assembly line {lines}')

print(f'*****************************************')
print(f'Maybe the same product can belong to different assembly lines and the person should decide where it should go:')
lines = fakeConnectionSAP.search_item(19092, fakeConnectionSAP.DB_NAME)
print(f'The product with identification 19092, belong to the assembly lines {lines}')
print(f'Or this can be automatized if a assembly line requires the piece so, inside of the options we select the '
      f'one that required the piece.')
