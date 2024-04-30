import sys
from pyteal import *
from daoutilities import DAOtokenName, DAOGovName

cmd=ScratchVar(TealType.bytes)

def handle_creation():
    return Approve()

def handle_optin():
    return Approve()

def handle_closeout():
    return Approve()

def handle_closeout():
    return Approve()

def handle_updateapp():
    return Approve()

def handle_deleteapp():
    return Approve()

def handle_noop():
    return Approve()


def approval_program(appId):

    program = Cond(
        [Txn.application_id()==Int(0), handle_creation()],
        [Txn.on_completion()==OnComplete.OptIn, handle_optin()],
        [Txn.on_completion()==OnComplete.CloseOut, handle_closeout()],
        [Txn.on_completion()==OnComplete.UpdateApplication, handle_updateapp()],
        [Txn.on_completion()==OnComplete.DeleteApplication, handle_deleteapp()],
        [Txn.on_completion()==OnComplete.NoOp, handle_noop()]
    )

    return compileTeal(program, Mode.Application, version=5)

if __name__=='__main__':
    if len(sys.argv)!=2:
        print("Usage: python",sys.argv[0],"<app ID>")
        exit()

    program=approval_program(sys.argv[1])
    with open("priceAcc.teal","w") as f:
        f.write(program)
