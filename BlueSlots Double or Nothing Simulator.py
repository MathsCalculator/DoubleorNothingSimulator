# Importing necessary modules
import random, os, time, math, subprocess, multiprocessing
# Custom exceptions for user interaction BOTH BRANCHES
class UserRetriesInput(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

class UserResetInputs(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

lineSeparator = "------------------------------------------------------------"

# Function to convert seconds into human-readable time SINGLE THREAD BRANCH
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

# Function to print ETA during simulations SINGLE THREAD BRANCH
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

# Function to calculate ETA based on the overall simulation progress SINGLE THREAD BRANCH
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

# Function to get user input for simulation parameters BOTH BRANCHES
def GetUserInput():
    global simulationsAmount, multiplier, percentage, price, calculationsAmount, jackpot, totalSimulationsAmount, decimalPlaces, targetPercentage
    correctInputs = 0
    chancePerSim = None
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
                    raise UserRetriesInput()
                multiplier = int(multiplier)
                if multiplier > 9 or multiplier < 1:
                    raise ValueError(f"Value '{multiplier}' of type '{type(multiplier)}' is not in range(1-9)")
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
                        raise UserRetriesInput()
                    jackpot = int(jackpot)
                    if jackpot < 0:
                        raise ValueError(f"Value '{jackpot}' of type '{type(jackpot)}' can not be negative")
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
                    raise UserRetriesInput()
                calculationsAmount = int(calculationsAmount)
                if calculationsAmount <= 0:
                    raise ValueError(f"Value '{calculationsAmount}' of type '{type(calculationsAmount)}' can not be negative")
                correctInputs = 3
                if calculationsAmount < os.cpu_count() and doMultithread:
                    os.system('cls')
                    print(f"Note: It is recommended to use more calculations than you have threads for optimal time and result ratio\nYou have {os.cpu_count()} threads\n\n")
                    input("Press enter to continue")
                    raise UserRetriesInput()
            else:
                print(f"Amount of calculations: {calculationsAmount}")
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
                    raise UserRetriesInput()
                simulationsAmount = int(simulationsAmount)
                if simulationsAmount <= 0:
                    raise ValueError(f"Value '{simulationsAmount}' of type '{type(simulationsAmount)}' can not be negative")
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
                    raise UserRetriesInput()
                percentage = float(percentage)
                if percentage <= 0 or percentage > 100:
                    raise ValueError(f"Value '{percentage}' of type '{type(percentage)}' is not in range(0-100)")
                chancePerSim = (((percentage / 100) ** multiplier) * 100)
                os.system('cls')
                if AskOrCheckYesNo(f"The chance of reaching X{multiplier} is {chancePerSim}%\nContinue with this percentage? (y/n): "):
                    correctInputs = 5
                    raise UserRetriesInput()
                else:
                    raise UserRetriesInput()
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
                raise UserRetriesInput()
            price = int(price)
            if price < 1:
                raise ValueError(f"Value '{price}' of type '{type(price)}' is not larger than 0")
            break
        except TypeError as e:
            input(f"Error: {e}")
            os.system('cls')
        except ValueError as e:
            input(f"Error: {e}")
            os.system('cls')
        except UserRetriesInput:
            os.system('cls')
        except UserResetInputs:
            correctInputs = 0
            os.system('cls')

    # Declare some variables for other functions, pretty straight forward
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

# Function to convert seconds into human-readable time BOTH BRANCHES
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

# Function to get a y/n input BOTH BRANCHES
def AskOrCheckYesNo(value, passingOnInput = False):
    while True and not passingOnInput:
        try:
            userInput = str(input(value))
            if userInput.lower() == "y":
                return True
            elif userInput.lower() == "n":
                return False
            raise ValueError(f"Value '{userInput}' is not 'y' or 'n'")
        except ValueError as e:
            print(f"Error: {e}")
    while True and passingOnInput:
        try:
            if value.lower() == "y":
                return True
            elif value.lower() == "n":
                return False
            else:
                raise ValueError(f"Value '{value}' is not 'y' or 'n'")
        except ValueError as e:
                print(f"Error: {e}")

# Function to ask the user about logging results BOTH BRANCHES
def AskToLog():
    global logfile
    try:
        if AskOrCheckYesNo("Would you like to log the results? (y/n): "):
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

# Function to start the simulation process SINGLE THREAD BRANCH
def LSimulate(args):
    global grandTotalAttempts, attemptsInSec
    decimalPlaces, targetPercentage, multiplier, jackpot, price, simulationsAmount, currentCalc = args
    print(f"Calculating #{currentCalc}{' ' * 50}")
    if currentCalc != 0:
        GetSimulationsProcessETA(True)
    attempts = 0
    totalWon = 0
    totalLost = 0
    for _ in range(0, simulationsAmount):
        attempts = 0
        while True:
            isOk = True
            attempts += 1
            grandTotalAttempts += 1
            attemptsInSec += 1
            GetSimulationsProcessETA(False)
            for _ in range(0, multiplier):
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

    print(f'{format(calcTotalWon, ",d")}$ with {format(attempts, ",d")} total attempts{" " * 50}')
    return [calcTotalWon, attempts]

# Function to start the simulation process Multi-Threading BRANCH
def MSimulate(args):
    decimalPlaces, targetPercentage, multiplier, jackpot, price, simulationsAmount, currentCalc, queue = args
    queue.put(currentCalc)
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

    print(f"Calculation {currentCalc}:{' ' * 50}")
    print(f"{format(calcTotalWon, ',d')}$ with {format(attempts, ',d')} total attempts{' ' * 50}")
    queue.put(currentCalc)
    return [calcTotalWon, attempts]

# Function to calculate the required number of simulations BOTH BRANCHES
def GetRequiredSimulationsAmount(chancePerSim):
    requiredSimulationsAmount = GetTotalSimulationsAmount() * (100 / chancePerSim)
    return math.ceil(requiredSimulationsAmount)

# Function to calculate the total number of simulations BOTH BRANCHES
def GetTotalSimulationsAmount():
    totalSims = simulationsAmount * calculationsAmount
    return totalSims

# Function to reset variables for a new simulation NON MULTITHREAD BRANCH
def ResetVariables():
    global grandTotalAttempts, initialTime, days, hours, minutes, seconds, attemptsInSec, maxTime
    # Also declares the variables (some of them at least)
    grandTotalAttempts = 0
    initialTime = 0
    days, hours, minutes = 0.0, 0.0, 0.0
    seconds = None
    attemptsInSec = 0
    maxTime = 0

def PoolManager(queue, totalCalcs, timeStarted):
    activeCalcs = []
    finishedCalcs = []
    startedTasks = 0
    while startedTasks < totalCalcs * 2: # Times 2 because I basically call PoolManager twice per calculation, so each calculation will append startedTasks twice instead of once
        calcID = queue.get()
        if calcID in activeCalcs:
            activeCalcs.remove(calcID)
            finishedCalcs.append(calcID)
        else:
            activeCalcs.append(calcID)
        startedTasks += 1
        finishedCalcsNum = len(finishedCalcs)
        activeCalcsNum = len(activeCalcs)
        if finishedCalcsNum > 0 and finishedCalcsNum > activeCalcsNum * 1.5: # activeCalcsNum SHOULD be a constant value
            tasksInXTime = (time.time() - timeStarted) / finishedCalcsNum
            timeForAllTasks = GetTotalTimeTaken(tasksInXTime * (totalCalcs - finishedCalcsNum))
        else:
            timeForAllTasks = "N/A"
        print(f"Active threads: {activeCalcsNum} | {finishedCalcsNum}/{totalCalcs} finished | ETA: {timeForAllTasks}{' ' * 50}", end="\r")
        
# Main function to start the simulation program BOTH BRANCHES
def StartProgram():
    if not doMultithread:
        ResetVariables()
    GetUserInput()
    timeStarted = time.time()
    grandTotal = 0
    grandTotalAttempts = 0
    calcFeedbacks = []
    estimatedTimeTaken = None
    totalTimeTaken = None
    if doMultithread:
        queue = multiprocessing.Manager().Queue()
        tasks = [(decimalPlaces, targetPercentage, multiplier, jackpot, price, simulationsAmount, i + 1, queue) for i in range(calculationsAmount)]
        # Start a separate process to monitor the queue
        monitor_process = multiprocessing.Process(target=PoolManager, args=(queue, calculationsAmount, timeStarted))
        monitor_process.start()

        with multiprocessing.Pool() as pool:
            results = pool.map(MSimulate, tasks)

        monitor_process.join()

        for i, result in enumerate(results):
            calcTotalWon = result[0]
            calcTotalAttempts = result[1]

            grandTotal += calcTotalWon
            grandTotalAttempts += calcTotalAttempts

            calcFeedbacks.append(f"Calculation {i + 1}:\n{format(calcTotalWon, ',d')}$ with {format(calcTotalAttempts, ',d')} total attempts{' ' * 50}")
    else:
        for i in range(0, calculationsAmount):
            result = LSimulate(args = (decimalPlaces, targetPercentage, multiplier, jackpot, price, simulationsAmount, i + 1))
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
    if not doMultithread:
        print(lineSeparator)
    print(f"Total time taken: {tempTimeTakenVar}")
    if not doMultithread:
        estimatedTimeTaken = GetTotalTimeTaken(maxTime)
        print(f"Estimated time: {estimatedTimeTaken}")

    print(lineSeparator)

    if not doMultithread:
        totalTimeTaken = GetTotalTimeTaken(timeFinished - timeStarted)
        if totalTimeTaken == estimatedTimeTaken:
            print(f"ETA was ~100% accurate")
        elif round(timeFinished - timeStarted) < round(maxTime):
            print(f"ETA was {math.floor((round(timeFinished - timeStarted) / round(maxTime)) * 10000) / 100}% accurate")
        else:
            print(f"ETA was {math.floor((round(maxTime) / round(timeFinished - timeStarted)) * 10000) / 100}% accurate")

    # Ask user to log and log if approved
    if AskToLog():
        logs = open(logfile, "a+")
        # Log the user parameters input
        logs.write(f'When to cash in: 1-9 (9 = jackpot): {str(multiplier)}\nJackpot amount: {str(jackpot)}\nSims per calculation: {str(simulationsAmount)}\nAmount of calculations: {str(calculationsAmount)}\nWin rate percentage: {str(percentage)}\nPrice per use: {str(price)}\n\n')
        # Log all the feedback lines of the calcs and sims
        for tempresult in calcFeedbacks:
            logs.write(f'{str(tempresult.strip())}\n')
        # Log the resulting data of the completed simulation
        if grandTotal > 0:
            tempresult = f'\nTotal profit: {format(grandTotal, ",.2f")}$\nAverage profit per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ",.0f")}$\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{lineSeparator}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{lineSeparator}\nTotal time taken: {tempTimeTakenVar}'
            logs.write(f'{str(tempresult)}\n')
        if grandTotal < 0:
            tempresult = f'\nTotal loss: {format(abs(grandTotal), ",.2f")}$\nAverage loss per simulation: {format(round(abs(grandTotal / GetTotalSimulationsAmount())), ",.0f")}$\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{lineSeparator}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{lineSeparator}\nTotal time taken: {tempTimeTakenVar}'
            logs.write(f'{str(tempresult)}\n')
        logs.close()
        
        # Check if the user wants to open the "Logs" folder
        if AskOrCheckYesNo("Open logs folder? (y/n): "):
            # Construct the absolute path to the "Logs" folder relative to the script location
            logs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
            # Open the "Logs" folder using the file explorer
            subprocess.Popen(['explorer', logs_folder])
    input("Press enter to retry")
    os.system('cls')
    GetBranchToUse()
    os.system('cls')
    StartProgram()

# Function to print program information to the user
def PrintInfo():
    os.system('cls')
    print("This program simulates a player continuously using the Double or Nothing slot machine\n"
          "Just choose your settings and conditions and the program will start the simulations\nYou can reset your previous input(s) by typing 'reset' when asked any parameter\n"
          "If you need an explanation with a condition, type 'help'\nYou can log your results when the program is finished if necessary\n"
          "For feedback or bug reports, contact me on discord: mathscalculator\n")
    print("Multi-Threading info:\nEach calculation uses its own CPU core to run, so use multiple calculations\nYour PC might also slow down due to that fact")
    input("\nPress enter to continue")
    os.system('cls')

def GetBranchToUse(addNote = False):
    global doMultithread
    if addNote:
        print("This program has 2 branches:\n* Multi-Threading: Uses multiple CPU cores/threads ---> FASTER | Somewhat accurate ETA | Use multiple calculations\n* Single-Threaded: Uses 1 core/thread ---> SLOWER | Very accurate ETA\n")
    userChoice = AskOrCheckYesNo("Enable Multi-Threading? (y/n): ", False)

    if userChoice:
        os.system("cls")
        print("Multi-Threading enabled...")
        time.sleep(0.5)
        os.system("cls")
        doMultithread = True
    else:
        os.system("cls")
        print("Multi-Threading disabled...")
        time.sleep(0.5)
        os.system("cls")
        doMultithread = False

# Entry point of the program
if __name__ == "__main__":
    PrintInfo()
    GetBranchToUse(True)
    StartProgram()
