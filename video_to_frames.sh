DIR=$1
for folder in "$DIR"/*
do
  rm -rf "$folder/norm"
  rm -rf "$folder/therm"
  files=("$folder"/*)
  mkdir "$folder/norm"
  mkdir "$folder/therm"
  echo "Processing file ${files[1]}..."
  ffmpeg -i "${files[1]}" -vf fps=2 "$folder/norm/%03d.png"
  echo "Processing file ${files[2]}..."
  ffmpeg -i "${files[2]}" -vf fps=2 "$folder/therm/%03d.png"
done