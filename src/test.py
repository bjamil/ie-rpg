def set_text(text):
    alltext = []
    LINE_SIZE = 60
    for line in text.split("\n"):
        if len(line) <= LINE_SIZE :
            alltext.append(line)
        else:
            start = 0 # start index ( to avoid cutting off words )
            end = LINE_SIZE + 1

            while start < len(line):
                substr = line[start:end]

                # if the last character is not an empty space,
                # find the last end of word token and split the
                # line at that point
                if substr[-1] != ' ' and len(substr) == LINE_SIZE:
                    end = start+substr.rfind(' ') + 1

                # if we couldn't find a space in this line , revert
                # to our old end point
                if end == 0:
                    end = start+LINE_SIZE + 1

                # add the substring to our growing list
                print start, end, len(line), line[start:end].strip()
                alltext.append(line[start:end].strip())
                
                # set up the new start and end points 
                start = end
                end = start + LINE_SIZE + 1
                


a = "Hello Traveler! \nPress the Space-bar button to shoot at the boulders and clear your path!"
set_text(a)
