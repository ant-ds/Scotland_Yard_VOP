with open('mergedResults.txt', 'w') as merge:
    with open('analysis.txt', 'r') as ifp:
        lines = ifp.readlines()
        merge.writelines(lines)
    
    merge.write('\n')
    
    with open('analysisLaptop.txt', 'r') as ifp:
        lines = ifp.readlines()
        merge.writelines(lines)
