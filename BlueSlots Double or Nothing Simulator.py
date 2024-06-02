# Importing necessary modules
import random, os, time, math, winsound, subprocess, multiprocessing, threading

# Custom exceptions for user interaction
class UserAskedHelp(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

class UserResetInputs(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

lineSeparator = "------------------------------------------------------------"

# Function to get user input for simulation parameters
def GetUserInput():
    global simulationsAmount, multiplier, percentage, price, calculationsAmount, jackpot, totalSimulationsAmount, decimalPlaces, targetPercentage
    correctInputs = 0
    while True:
        try:
            # Multiplier
            if correctInputs < 1:
                multiplier = input("When to cash in: 1-9 (9 = jackpot): ")
                if multiplier.lower() == "reset":
                    raise UserResetInputs()
                if multiplier.lower() == "help":
                    os.system('cls')
                    print("This simulates a 'player' continuously playing the machine.\nSet player can cash in at any time.\nBy choosing 1, the 'player' will always cash in at 2X.\nBy choosing 9, the 'player' will go for jackpot (9X).")
                    input("\nPress enter to continue")
                    raise UserAskedHelp()
                multiplier = int(multiplier)
                if multiplier > 9 or multiplier < 1:
                    raise ValueError(f"Value {multiplier} of type {type(multiplier)} is not in range(1-9)")
                correctInputs = 1
            else:
                print(f"When to cash in: 1-9 (9 = jackpot): {multiplier}")
            # Jackpot
            if multiplier == 9:
                if correctInputs < 2:
                    jackpot = input("Jackpot amount: ")
                    if jackpot.lower() == "reset":
                        raise UserResetInputs()
                    if jackpot.lower() == "help":
                        os.system('cls')
                        print("The jackpot is the amount of money the 'player' will receive upon reaching 9X.")
                        input("\nPress enter to continue")
                        raise UserAskedHelp()
                    jackpot = int(jackpot)
                    if jackpot < 0:
                        raise ValueError(f"Value {jackpot} of type {type(jackpot)} can not be negative")
                    correctInputs = 2
                else:
                    print(f"Jackpot amount: {jackpot}")
            else:
                jackpot = None
            # Calculation amount
            if correctInputs < 3:
                calculationsAmount = input("Amount of calculations: ")
                if calculationsAmount.lower() == "reset":
                    raise UserResetInputs()
                if calculationsAmount.lower() == "help":
                    os.system('cls')
                    print(f"The program will have calculations and simulations.\nEvery calculation has an amount of simulations inside them.\nSay you chose 5 calculations and 2 simulations:\nThe program will then do 10 total simulations of a player reaching {multiplier}X.\n")
                    print(f"These will be separated like this:\n")
                    for i in range(0, 5):
                        print(f"Calculation #{i+1} <--- (CALCULATION {i+1})\n...$ with ... total attempts <--- (2 SIMULATIONS)")
                    print("Using 20+ calculations is recommended for better results.\n")
                    print("Warning: Low percentage and/or high amount of simulations/calculations will affect simulation speed\n")
                    input("Press enter to continue")
                    raise UserAskedHelp()
                calculationsAmount = int(calculationsAmount)
                if calculationsAmount <= 0:
                    raise ValueError(f"Value {calculationsAmount} of type {type(calculationsAmount)} can not be negative")
                correctInputs = 3
            else:
                print(f"Amount of calculations= {calculationsAmount}")
            # simulationsAmount
            if correctInputs < 4:
                simulationsAmount = input("Amount of simulations: ")
                if simulationsAmount.lower() == "reset":
                    raise UserResetInputs()
                if simulationsAmount.lower() == "help":
                    os.system('cls')
                    print(f"The program will have calculations and simulations.\nEvery calculation has an amount of simulations inside them.\nSay you chose 5 calculations and 2 simulations:\nThe program will then do 10 total simulations of a player reaching {multiplier}X.\n")
                    print(f"These will be separated like this:\n")
                    for i in range(0, 5):
                        print(f"Calculation #{i+1} <--- (CALCULATION {i+1})\n...$ with ... total attempts <--- (2 SIMULATIONS, they're summed up together)")
                    print("Using 20+ simulations is recommended for better results.\n")
                    print("Warning: Low percentage and/or high amount of simulations/calculations will affect simulation speed\n")
                    input("Press enter to try again")
                simulationsAmount = int(simulationsAmount)
                if simulationsAmount <= 0:
                    raise ValueError(f"Value {simulationsAmount} of type {type(simulationsAmount)} can not be negative")
                correctInputs = 4
            else:
                print(f"Amount of simulations: {simulationsAmount}")
            # Percentage
            if correctInputs < 5:
                percentage = input("Win rate percentage (per attempt): ")
                if percentage.lower() == "reset":
                    raise UserResetInputs()
                if percentage.lower() == "help":
                    os.system('cls')
                    print("The chance of going from 2X to 3X or from 3X to 4X etc.\nPercentage can be a float or int\n")
                    print("Warning: Low percentage and/or high amount of simulations/calculations will affect simulation speed\n")
                    input("Press enter to continue")
                    raise UserAskedHelp()
                percentage = float(percentage)
                if percentage <= 0 or percentage > 100:
                    raise ValueError(f"Value {percentage} of type {type(percentage)} is not in range(0-100)")
                correctInputs = 5
            else:
                print(f"Win rate percentage (per attempt): {percentage}")
            # Price
            price = input("Price per use: ")
            if price.lower() == "reset":
                raise UserResetInputs()
            if price.lower() == "help":
                os.system('cls')
                print("The price the user would have to pay every time he starts another game.\nUser pays every time he starts from 1X (multiple times per simulation).")
                input("\nPress enter to continue")
                raise UserAskedHelp()
            price = int(price)
            if price < 1:
                raise ValueError(f"Value {price} of type {type(price)} is not larger than 0")
            break
        except TypeError as e:
            input(f"Error: {e}")
            os.system('cls')
        except ValueError as e:
            input(f"Error: {e}")
            os.system('cls')
        except UserAskedHelp:
            os.system('cls')
        except UserResetInputs:
            correctInputs = 0
            os.system('cls')

    # Declare some global variables for other functions
    chancePerSim = (((percentage / 100) ** multiplier) * 100)
    totalSimulationsAmount = GetRequiredSimulationsAmount(chancePerSim)
    print("Winning chance per simulation: ", chancePerSim, "%")
    print("Average amount of simulations: ", format(totalSimulationsAmount, ",d"))
    if '.' in str(percentage):
        decimalPosition = str(percentage).index('.')
        decimalPlaces = (len(str(percentage)) - decimalPosition - 1) + 2
    else:
        decimalPlaces = 2
    targetPercentage = int(str(percentage).replace(',', '').replace('.', ''))
    print(lineSeparator)
    print("Calculating...", end="\r")

# Function to convert seconds into human-readable time
def GetTotalTimeTaken(seconds):
    # List of time units and their corresponding seconds
    units = [
        ('year', 86400 * 7 * 52.178),
        ('month', 86400 * 7 * 4.348),
        ('week', 86400 * 7),
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
        ('second', 1)
    ]
    result = []
    # Iterate over units to build the time representation
    for unitName, unitSeconds in units:
        if seconds >= unitSeconds:
            unitCount = round(seconds / unitSeconds)
            seconds %= unitSeconds
            if unitCount > 1:
                result.append(f"{unitCount} {unitName}s")
            else:
                result.append(f"{unitCount} {unitName}")
    # Format the result
    if result:
        return ', '.join(result)
    else:
        return "0 seconds"

# Function to get a y/n input
def AskYesNo(question):
    while True:
        try:
            userInput = str(input(question))
            if userInput.lower() == "y":
                return True
            elif userInput.lower() == "n":
                return False
            raise ValueError(f"Value {userInput} is not 'y' or 'n'")
        except ValueError as e:
            print(f"Error: {e}")

# Function to ask the user about logging results
def AskToLog():
    global logfile
    try:
        if AskYesNo("Would you like to log the results? (y/n): "):
            logsPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
            if not os.path.exists(logsPath):
                os.makedirs(logsPath)
            i = len(os.listdir(logsPath)) + 1
            logfile = os.path.join(logsPath, f"log_{i}.txt")
            # Create an empty file if it doesn't exist
            if not os.path.exists(logfile):
                with open(logfile, 'a'):
                    os.utime(logfile, None)  # Create an empty file if it doesn't exist
            print(f"Created {logfile}")
            return True
        return False
    except Exception as e:
        print(f"Logging disabled due to error: {e}")
    return False

# Function to start the simulation process
def MSimulate(args):
    decimalPlaces, targetPercentage, multiplier, jackpot, price, simulationsAmount, currentCalc = args
    attempts = 0
    totalWon = 0
    totalLost = 0
    for _ in range(0, simulationsAmount):
        while True:
            isOk = True
            attempts += 1
            for i in range(0, multiplier):
                if not random.randint(0, 10 ** decimalPlaces) <= targetPercentage:
                    isOk= False
            if isOk is True:
                break
        if multiplier == 9:
            totalWon += jackpot
        else:
            totalWon += price * (2 ** multiplier)
    totalLost = price * attempts

    calcTotalWon = totalWon - totalLost

    print(f"Calculation {currentCalc}:")
    print(f"{format(calcTotalWon, ',d')}$ with {format(attempts, ',d')} total attempts")
    return [calcTotalWon, attempts]

# Function to calculate the required number of simulations
def GetRequiredSimulationsAmount(chancePerSim):
    requiredSimulationsAmount = GetTotalSimulationsAmount() * (100 / chancePerSim)
    return math.ceil(requiredSimulationsAmount)

# Function to calculate the total number of simulations
def GetTotalSimulationsAmount():
    totalSims = simulationsAmount * calculationsAmount
    return totalSims

# Main function to start the simulation program
def StartMProgram():
    GetUserInput()

    calcFeedbacks = []

    grandTotal = 0
    grandTotalAttempts = 0

    tasks = [(decimalPlaces, targetPercentage, multiplier, jackpot, price, simulationsAmount,  i + 1) for i in range(calculationsAmount)]

    timeStarted = time.time()
    with multiprocessing.Pool() as pool:
        results = pool.map(MSimulate, tasks)

    for i, result in enumerate(results):
        calcTotalWon = result[0]
        calcTotalAttempts = result[1]

        grandTotal += calcTotalWon
        grandTotalAttempts += calcTotalAttempts

        calcFeedbacks.append(f"Calculation {i + 1}:\n{format(calcTotalWon, ',d')}$ with {format(calcTotalAttempts, ',d')} total attempts{' ' * 50}")
    timeFinished = time.time()
    print(lineSeparator)
    # Print all results to user
    if grandTotal > 0:
        print(f"Total profit: {format(grandTotal, ',d')}$")
        print(f"Average profit per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ',.0f')}$")
    if grandTotal < 0:
        print(f"Total loss: {format(abs(grandTotal), ',d')}")
        print(f"Average loss per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ',.0f')}$")
    print(f"Average attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ',.0f')}")
    print(lineSeparator)
    print(f"Total calculations done: {format(abs(grandTotalAttempts), ',d')}")
    print(f"Estimated calculations: {format(abs(totalSimulationsAmount), ',d')}")
    tempTimeTakenVar = ""
    if timeFinished - timeStarted < 60:
        tempTimeTakenVar = str(round((timeFinished - timeStarted) * (10 ** 2)) / (10 ** 2)) + " seconds"
    else:
        tempTimeTakenVar = GetTotalTimeTaken(timeFinished - timeStarted)
    print(f"Total time taken: {tempTimeTakenVar}")
    print(lineSeparator)
    # Ask user to log and log if approved
    if AskToLog():
        logs = open(logfile, "a+")
        # Log the user parameters input
        logs.write(f'When to cash in: 1-9 (9 = jackpot): {str(multiplier)}\nJackpot amount: {str(jackpot)}\nSims per calculation: {str(simulationsAmount)}\nAmount of calculations: {str(calculationsAmount)}\nWin rate percentage: {str(percentage)}\nPrice per use: {str(price)}\n\n')
        # Log all the feedback lines of the calcs and sims
        for tempresult in calcFeedbacks:
            logs.write(f'{str(tempresult)}\n')
        # Log the resulting data of the completed simulation
        if grandTotal > 0:
            tempresult = f'\nTotal profit: {format(grandTotal, ",.2f")}$\nAverage profit per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ",.0f")}$\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{lineSeparator}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{lineSeparator}\nTotal time taken: {tempTimeTakenVar}'
            logs.write(f'{str(tempresult)}\n')
        if grandTotal < 0:
            tempresult = f'\nTotal loss: {format(abs(grandTotal), ",.2f")}$\nAverage loss per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ",.0f")}$\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{lineSeparator}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{lineSeparator}\nTotal time taken: {tempTimeTakenVar}'
            logs.write(f'{str(tempresult)}\n')
        logs.close()
        
        # Check if the user wants to open the "Logs" folder
        if AskYesNo("Open logs folder? (y/n): "):
            # Construct the absolute path to the "Logs" folder relative to the script location
            logs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
            # Open the "Logs" folder using the file explorer
            subprocess.Popen(['explorer', logs_folder])
    input("Press enter to retry")
    os.system('cls')
    StartMProgram()

# Function to print program information to the user
def PrintInfo():
    os.system('cls')
    print("This program simulates a player continuously using the Double or Nothing slot machine\n"
          "Just choose your settings and conditions and the program will start the simulations\nYou can reset your previous input(s) by typing 'reset' when asked any parameter\n"
          "If you need an explanation with a condition, type 'help'\nYou can log your results when the program is finished if necessary\n"
          "For feedback or bug reports, contact me on discord: mathscalculator\n\nEach calculation uses it's own CPU core to run, so it is recommended to use 20+ calculations\nYour PC might also slow down due to that fact")
    input("\nPress enter to continue")
    os.system('cls')

# Entry point of the program
if __name__ == "__main__":
    PrintInfo()
    StartMProgram()
