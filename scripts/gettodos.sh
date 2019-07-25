#!/usr/bin/env bash
cd ~/code/multiplayer-game-base/
FILE=TODOS.txt
echo "" > /tmp/TODOS.txt
[ -f $FILE ] && { cp "$FILE" /tmp/; }


echo "Setting Todos File"
# Title
awk  'BEGIN{
    for(c=0;c<55;c++) printf "="f; printf("\n")
    print "TODOS IN PROJECT: Multiplayer-Game-Base";

    for(c=0;c<55;c++) printf "=";
    printf("\n\n");
    for(c=0;c<55;c++) printf "=";
    printf("\n")
    print "TODO LIST"
    for(c=0;c<55;c++) printf "=";
    printf("\n")
}
' TODOS.txt > TODOS.txt
# awk '{for(c=0;c<55;c++) printf "=";}' TODOS.txt >> TODOS.txt
awk '/[ \t]---/{print$0;}END{for(c=0;c<55;c++) printf "=";
    printf("\n\n\n")}' /tmp/TODOS.txt >> TODOS.txt

grep -r -i "TODO" ./src | awk '
BEGIN {
    for(c=0;c<55;c++) printf "="f; printf("\n")
    print "Front-END TODOS";
    for(c=0;c<55;c++) printf "="f; printf("\n")
}
"://"{
    gsub("://", ":", $0);
}
{

    comment = substr($0, index($0,$2));
    path = $1;
    printf path;
    gsub(path,"",$0);
}

/^[ \t]+/{
    gsub(/^[ \t]+/, "", $0)
    
}

/^\/\//{gsub("//","",$0)}
/^[ \t]*/{gsub("^[ \t]+", "",$0)}
{

    
    {gsub(/^TODO[:]?[ \t]?/, "", $0); printf "\n    -" $0 }
    printf "\n";


} 
END {
   printf("\n")
} ' >> TODOS.txt

grep -r -i -E "(\/\/\?)" --include="*.js" --include="*.jsx" ./src | awk '
BEGIN {
    for(c=0;c<55;c++) printf "="f; printf("\n")
    print "Front-END Queries";
    for(c=0;c<55;c++) printf "="f; printf("\n")
}
{
    
    {gsub("://?", " ", $0);}
    path = $1;
    print path;


    {gsub(path,"",$0); gsub(/^[?]?[ \t]+/, "", $0); printf "    -" $0 }
    printf "\n";


} 
END {
    for(c=0;c<55;c++) printf "="f; printf("\n\n\n")
} ' >> TODOS.txt


grep -r -i "TODO" ./flask_server | awk '
BEGIN {
    for(c=0;c<55;c++) printf "="f; printf("\n")
    print "BACK-END TODOS";
    for(c=0;c<55;c++) printf "="f; printf("\n")
}
{
    {gsub("#", " ",$0)}

    comment = substr($0, index($0,$2));
    path = $1;

    {gsub(path, "", $0)}
    printf path;
    {gsub(path,"",$0);gsub(/[ \t]+TODO[:]?[ \t]?/,"",$0);  printf "\n    -" $0 }
    printf "\n";

} 
END {
    for(c=0;c<55;c++) printf "="f; printf("\n\n")

} ' >> TODOS.txt
# fmt --w 55 -s TODOS.txt > _TODOS.txt
# awk '!seen[$0]++ || /([=]+)/ || !NF' _TODOS.txt > TODOS.txt
# rm _TODOS.txt
