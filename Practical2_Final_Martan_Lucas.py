#Saving Cents
#BY:    Martan van der Straaten
#       Lucas van Kasteren   

#Includes
import sys

#function to round our values to the nearest 5.
def getRounded(value):
    # get last digit of value
    x = value%10

    # case distinction
    if (x==1 or x==2):
        return value - x
    elif (x== 3 or x == 4):
        return value + (5-x)
    elif (x == 6 or x == 7):
        return value - x + 5
    elif (x==8 or x== 9):
        return value + (10-x)
    else:
        return value

def getBest(start_index, nr_dividers, nr_products, MATRIX, LOOKUP_TABLE):
    # Base case:
    # We have no dividers so just take the sum and round it.
    if (nr_dividers == 0):
        return MATRIX[start_index][nr_products-1]

    # Default case:
    # This is the default value we can get. It might be that we can improve on it, or we might not be able to
    # Either way, this is a good initial value.
    best = MATRIX[start_index][nr_products-1]
    
    # Recursive cases:
    # Try to place a divider at each index of the current slice
    for i in range(start_index+1, nr_products):
        # Calculate the total value of the products in the slice that are left of the divider, if we place it at index i.
        left = MATRIX[start_index][i-1]
        # Initialize the total value of the products in the slice that are right of the divider, if we place it at index i with 0.
        right = 0
        
        # If we already found a solution for this situation where:
        # - i was the same
        # - nr_dividers was the same
        # Then we can just look in our LOOKUP_TABLE to find the solution in O(1)
        if(LOOKUP_TABLE[i][nr_dividers]>= 0):
            right = LOOKUP_TABLE[i][nr_dividers]

        # Otherwise, we recursively call the function, but we change start_index to i, and nr_dividers to nr_dividers-1
        else:
            # Recursive call
            right = getBest(i, nr_dividers-1, nr_products, MATRIX, LOOKUP_TABLE)
            #print()
            # We now store this solution at the appropriate spot in our lookup-table
            LOOKUP_TABLE[i][nr_dividers] = right
            
        # We get the new value by rounding the left and right side, and adding them
        new = left+getRounded(right)

        #We clearly cannot improve any further, so stop
        if (new > best):
            return best

        # If this new value is better than the current best value, new is our new best
        if(new< best):
            best= new

    # Return the overal best value
    return best

def getInput():
    counter = 0
    
    # Getting the problem from the server

    # Read NR_PRODUCTS and NR_DIVIDERS
    NR_PRODUCTS, NR_DIVIDERS = [int(x) for x in input().split(' ')]
    
    # Print to stderr, such that it does not influence the server
    print(f"NR_PRODUCTS:{NR_PRODUCTS} ", file=sys.stderr)
    print(f"NR_DIVIDERS:{NR_DIVIDERS} ", file=sys.stderr)

    # Base case, such that no time is wasted if this occurs
    if(NR_PRODUCTS == 0):
        print(0)
        return

    # Read products and store them in list, where the elements were seperated by spaces.
    Products_IN = input().split(' ')
    PRODUCTS = []
    
    # Store products as integers.
    for x in range(NR_PRODUCTS):
        PRODUCTS.append(int(Products_IN[x]))

    # MATRIX:
    # Create the matrix
    MATRIX = [[] for x in range(NR_PRODUCTS)]

    # Fill first row, each time adding one more value of a product to counter
    counter = 0
    for j in range(0, NR_PRODUCTS):
        counter += PRODUCTS[j]
        MATRIX[0].append(getRounded(counter))

    # Fill all other rows using information from previous rows
    for i in range(1,NR_PRODUCTS):
        counter = 0
        for j in range(0, NR_PRODUCTS):
            # Filling, but irrelevant this slice does not really exist
            if (j<i):
                MATRIX[i].append(-1)
            # Actual case, add to counter and append counter to the matrix
            else:
                counter += PRODUCTS[j]
                MATRIX[i].append(getRounded(counter))

    # LOOKUP TABLE
    # Fill in -1 (nonsense) for everything except last.
    LOOKUP_TABLE = [[-1 for x in range(NR_DIVIDERS+1)] for x in range(NR_PRODUCTS-1)]
    # Fill in last with the value of the last product.
    LOOKUP_TABLE.append([PRODUCTS[NR_PRODUCTS-1] for x in range(NR_DIVIDERS+1)])
    # Print result of the getBest() function, so the least amount we have to pay
    print(getBest(0, NR_DIVIDERS, NR_PRODUCTS, MATRIX, LOOKUP_TABLE))


def main():
    # Load and solve the problem
    getInput()


if __name__ == "__main__":
    main()
