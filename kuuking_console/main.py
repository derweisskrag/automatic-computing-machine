from src.kuuking_console.kuuking_console import KuukingConsoleMachine


def main():
    # Call Console
    kuuking_console_machine = KuukingConsoleMachine() 

    # Later we can add termination signals here and even config!
    # We can let users customize it
    # Call lambdas
    # But for now!
    # Just call the dam machine
    kuuking_console_machine.run() # Oh, I can feel it will... you know Burmese Python


if __name__ == "__main__":
    main()