from axiomtradeapi import AxiomTradeClient

def get_attrs():
    client = AxiomTradeClient()
    attrs = dir(client)
    return attrs

if __name__ == "__main__":
    attributes = get_attrs()
    for attr in attributes:
        print(attr)
    with open("client_attributes.txt", "w") as f:
        for attr in attributes:
            f.write(f"{attr}\n")
    print("Client attributes written to client_attributes.txt")