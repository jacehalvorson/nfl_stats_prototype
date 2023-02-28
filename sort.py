def quickSort( table, sortByCol, depth ):
   if len( table ) <= 1:
      # Base case - nothing to sort with 0 or 1 rows
      print( f'Sort bottomed out at depth {depth}' )
      return table
   
   # Partition into sublists based on the middle element
   partitionIndex = floor( len( table ) / 2 )
   partitionRow = table[ partitionIndex ]
   partitionValue = partitionRow[ sortByCol ]
   del table[ partitionIndex ]
   
   lessThanPartition = [ ]
   moreThanPartition = [ ]
   
   # Check each row except the partition row
   for row in table:
      value = row[ sortByCol ]
      if value[ 0 ].isdigit( ):
         # Value starts with a digit
         isValueLessThanPartitionValue = ( float( value ) < float( partitionValue ) )
      else:
         # Value starts with a letter
         # Flip compare direction so names start with A and end with Z
         isValueLessThanPartitionValue = ( value > partitionValue )

      if isValueLessThanPartitionValue:
         lessThanPartition.append( row )
      else:
         moreThanPartition.append( row )
      
   # Sort the sublists
   lessThanPartition = quickSort( lessThanPartition, sortByCol, depth+1 )
   moreThanPartition = quickSort( moreThanPartition, sortByCol, depth+1 )
   
   # Put back the partition row in between the sublists
   lessThanPartition.append( partitionRow )

   # Add the lesser sublist and return the result
   lessThanPartition.extend( moreThanPartition )
   return lessThanPartition

def mergeSort( table, sortByCol, depth ):
   # Base case
   if len( table ) <= 1:
      return table
   
   # Split table in half
   startIndexOfSecondTable = int( len( table ) / 2 )
   firstTable = table[ :startIndexOfSecondTable ]
   secondTable = table[ startIndexOfSecondTable: ]

   # Recursively sort the subtables
   firstTable = mergeSort( firstTable, sortByCol, depth+1 )
   secondTable = mergeSort( secondTable, sortByCol, depth+1 )
   
   # Merge the sorted subtables together
   firstIndex = 0
   secondIndex = 0
   mergeResult = [ ]
   while firstIndex + secondIndex < len( table ):
      # Bounds check the first index
      if firstIndex < len( firstTable ):
         firstTableCurrentRow = firstTable[ firstIndex ]
         firstTableCurrentValue = firstTableCurrentRow[ sortByCol ]
      else:
         mergeResult.extend( secondTable[ secondIndex: ] )
         break

      # Bounds check the second index
      if secondIndex < len( secondTable ):
         secondTableCurrentRow = secondTable[ secondIndex ]
         secondTableCurrentValue = secondTableCurrentRow[ sortByCol ]
      else:
         mergeResult.extend( firstTable[ firstIndex: ] )
         break

      # Compare the values in sortByCol to see which one should be added next
      if firstTableCurrentValue[ 0 ].isdigit( ) and float( firstTableCurrentValue ) != float( secondTableCurrentValue ):
         # Values start with a digit and they are not the same number
         isFirstLessThanSecond = ( float( firstTableCurrentValue ) < float( secondTableCurrentValue ) )
      else:
         # Compare player names and flip compare direction so names start with A and end with Z
         isFirstLessThanSecond = ( firstTable[ firstIndex ][ 0 ] > secondTable[ secondIndex ][ 0 ] )

      if isFirstLessThanSecond:
         mergeResult.append( firstTableCurrentRow )
         firstIndex += 1
      else:
         mergeResult.append( secondTableCurrentRow )
         secondIndex += 1
         
   return mergeResult