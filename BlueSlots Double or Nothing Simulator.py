# Copyright (c) [2023], [mathscalculator]

# Importing necessary modules
import random, os, time, math, winsound, subprocess

# Initializing global variables
totalAttempts = 0
totalSimulationsAmount = None
linesplit = "------------------------------------------------------------"
logfile = None

# Custom exceptions for user interaction
class UserAskedHelp(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

class UserResetInputs(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

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

# Function to print ETA during simulations
def PrintSimulationsProcessETA(i):
    global days, hours, minutes, seconds, maxTime
    seconds = i
    if seconds is None:
        return
    if maxTime < seconds:
        maxTime = seconds + 1
    days = seconds / 86400
    hours = (seconds % 86400) / 3600
    minutes = ((seconds % 86400) % 3600) / 60
    # Display ETA based on the duration of the simulation
    if seconds > (86400 * 7 * 52.178):
        years = seconds / (86400 * 7 * 52.178)
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(years, 2) * 10) / 10} year(s) (you will need a quantum computer){" " * 5}', end="\r")
    elif seconds > 86400 * 7 * 4.348:
        months = seconds / (86400 * 7 * 4.348)
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(months, 2) * 10) / 10} month(s) (you might need a quantum computer){" " * 5}', end="\r")
    elif seconds > 86400 * 7:
        weeks = seconds / (86400 * 7)
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(weeks, 2) * 10) / 10} week(s){" " * 50}', end="\r")
    elif seconds > (86400 * 2):
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(days, 2) * 10) / 10} days{" " * 50}', end="\r")
    elif seconds > 86400:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.floor(days)} day, {math.ceil(hours * 10) / 10} hr(s){" " * 50}', end="\r")
    elif seconds > 3600:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.floor(hours)} hr(s), {math.ceil(minutes)} min(s){" " * 50}', end="\r")
    elif seconds > 60:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(minutes * 10) / 10} min(s){" " * 50}', end="\r")
    else:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {round(seconds)} second(s){" " * 50}', end="\r")

# Function to calculate ETA based on the overall simulation progress
def GetSimulationsProcessETA(override):
    global attemptsInSec, initialTime
    if override is True:
        if totalSimulationsAmount < grandTotalAttempts:
            print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: Now{" " * 50}', end="\r")
        else:
            PrintSimulationsProcessETA(seconds)
    if (time.time() - initialTime) > 1 and initialTime != 0:
        if totalSimulationsAmount < grandTotalAttempts:
            print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: Now{" " * 50}', end="\r")
            initialTime = 0
        else:
            timeForTheRest = (time.time() - initialTime) * ((totalSimulationsAmount - grandTotalAttempts) / attemptsInSec)
            PrintSimulationsProcessETA(timeForTheRest)
            attemptsInSec = 0
            initialTime = 0
    elif initialTime == 0:
        initialTime = time.time()

# Function to calculate the required number of simulations
def GetRequiredSimulationsAmount(chancePerSim):
    requiredSimulationsAmount = GetTotalSimulationsAmount() * (100 / chancePerSim)
    return math.ceil(requiredSimulationsAmount)

# Function to calculate the total number of simulations
def GetTotalSimulationsAmount():
    totalSims = simulationsAmount * calculationsAmount
    return totalSims

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
                        print(f"Calculating #{i+1} <--- (CALCULATION {i+1})\n...$ with ... total attempts <--- (2 SIMULATIONS)")
                    print("Using 10+ calculations is recommended for better results.\n")
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
                        print(f"Calculating #{i+1} <--- (CALCULATION {i+1})\n...$ with ... total attempts <--- (2 SIMULATIONS)")
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
                print("The price the user has to pay every time he starts another game.\nUser pays every time he starts from 1X.")
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
    print("------------------------------------------------------------")

# Function to start the simulation process
def StartSimulating(numb):
    global totalAttempts, grandTotal, finishedCalculations, grandTotalAttempts, attemptsInSec, calcFeedbacks
    print(f"Calculating #{numb}", " " * 50)
    if finishedCalculations != 0:
        GetSimulationsProcessETA(True)
    finishedCalculations += 1
    attempts = 0
    totalWon = 0
    totalLost = 0
    totalAttempts = 0
    for i in range(0, simulationsAmount):
        attempts = 0
        while True:
            isOk = True
            totalAttempts += 1
            attempts += 1
            grandTotalAttempts += 1
            attemptsInSec += 1
            GetSimulationsProcessETA(False)
            for i in range(0, multiplier):
                if not random.randint(0, 10 ** decimalPlaces) <= targetPercentage:
                    isOk= False
            if isOk is True:
                break
        if multiplier == 9:
            totalWon = totalWon + jackpot
        else:
            totalWon += price * (2 ** multiplier)
        totalLost += price * attempts
    print(f'{format(totalWon - totalLost, ",d")}$ with {format(totalAttempts, ",d")} total attempts{" " * 50}')
    # Keep output in case of logging
    tempresult = f'{format(totalWon - totalLost, ",d")} with {format(totalAttempts, ",d")} total attempts'
    calcFeedbacks.append(tempresult)

    grandTotal += totalWon - totalLost

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
    if AskYesNo("Would you like to log the results? (y/n): "):
        if not os.path.exists("Logs"):
            os.makedirs("Logs")
        i = len(os.listdir("Logs")) + 1
        open('Logs\log_' + str(i) + '.txt', "w")
        logfile = 'Logs\log_' + str(i) + '.txt'
        print(f"Created Logs\log_{i}")
        return True
    return False

# Function to reset variables for a new simulation
def ResetVariables():
    global finishedCalculations, grandTotalAttempts, initialTime, days, hours, minutes, seconds, attemptsInSec, maxTime, grandTotal, calcFeedbacks
    # Also declares the variables (some of them at least)
    finishedCalculations = 0
    grandTotalAttempts = 0
    initialTime = 0
    days, hours, minutes = 0.0, 0.0, 0.0
    seconds = None
    attemptsInSec = 0
    maxTime = 0
    grandTotal = 0
    calcFeedbacks = []

# Main function to start the simulation program
def StartProgram():
    ResetVariables()
    GetUserInput()
    timeStarted = time.time()
    for i in range(0, calculationsAmount):
        StartSimulating(i + 1)
    timeFinished = time.time()
    print("\n")
    # Print all results to user
    if grandTotal > 0:
        print("Total profit:", format(grandTotal, ",d"), " " * 50)
        print(f"Average profit per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ',.0f')}")
    if grandTotal < 0:
        print("Total loss:", format(abs(grandTotal), ",d"), " " * 50)
        print(f"Average loss per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ',.0f')}")
    print(f"Average attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ',.0f')}")
    print(linesplit)
    print(f"Total calculations done: {format(abs(grandTotalAttempts), ',d')}")
    print(f"Estimated calculations: {format(abs(totalSimulationsAmount), ',d')}")
    print(linesplit)
    totalTimeTaken = GetTotalTimeTaken(timeFinished - timeStarted)
    estimatedTimeTaken = GetTotalTimeTaken(maxTime)
    print(f"Total time taken: {totalTimeTaken}")
    print(f"Estimated time: {estimatedTimeTaken}")
    print(linesplit)
    print(timeFinished - timeStarted)
    print(maxTime)
    if totalTimeTaken == estimatedTimeTaken:
        print(f"ETA was ~100% accurate")
    elif round(timeFinished - timeStarted) < round(maxTime):
        print(f"ETA was {math.floor((round(timeFinished - timeStarted) / round(maxTime)) * 10000) / 100}% accurate")
    else:
        print(f"ETA was {math.floor((round(maxTime) / round(timeFinished - timeStarted)) * 10000) / 100}% accurate")
    # Ask user to log and log if approved
    if AskToLog():
        logs = open(logfile, "a")
        # Log the user parameters input
        logs.write(f'Number: {str(multiplier)}\nJackpot amount: {str(jackpot)}\nSims per calculation: {str(simulationsAmount)}\nAmount of calculations: {str(calculationsAmount)}\nWin rate percentage: {str(percentage)}\nPrice per use: {str(price)}\n\n')
        # Log all the feedback lines of the calcs and sims
        for tempresult in calcFeedbacks:
            logs.write(f'{str(tempresult)}\n')
        # Log the resulting data of the completed simulation
        if grandTotal > 0:
            tempresult = f'\nTotal profit: {format(grandTotal, ",.2f")}\nAverage profit per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ",.0f")}\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{linesplit}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{linesplit}\nTotal time taken: {GetTotalTimeTaken(timeFinished - timeStarted)}'
            logs.write(f'{str(tempresult)}\n')
        if grandTotal < 0:
            tempresult = f'\nTotal loss: {format(abs(grandTotal), ",.2f")}\nAverage loss per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ",.0f")}\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{linesplit}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{linesplit}\nTotal time taken: {GetTotalTimeTaken(timeFinished - timeStarted)}'
            logs.write(f'{str(tempresult)}\n')
        logs.close()
        winsound.PlaySound(os.environ['SystemDrive'] + '\Windows\Media\Windows Background.wav', winsound.SND_ALIAS)
        if AskYesNo("Open logs folder? (y/n): "):
            subprocess.Popen(['explorer', 'Logs'], shell=True)
    input("Press enter to retry")
    os.system('cls')
    StartProgram()

# Function to print program information to the user
def PrintInfo():
    os.system('cls')
    print("Welcome to the BlueSlots Double or Nothing simulator\nThis program simulates a player continuously using the Double or Nothing slot machine\n"
          "Just choose your settings and conditions and the program will start the simulations\nYou can reset your input by typing 'RESET' when asked any parameter\n"
          "If you need an explanation with a condition, type 'HELP'\nYou can log your results when the program is finished if necessary\n"
          "For feedback or bug reports, contact me on discord: mathscalculator\n(ETA rounds the numbers, might be slighty inaccurate)")
    input("\nPress enter to continue")
    os.system('cls')

# Entry point of the program
if __name__ == "__main__":
    PrintInfo()
    StartProgram()