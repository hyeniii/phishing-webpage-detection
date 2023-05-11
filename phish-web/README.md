# fast-api port : 8000
# react app port : 3000

```bash
docker build -t <yourname/projectname> .

# d flag is for detached mode where the website will 
#run on the background without interupting your terminal
docker run -d -t -p 3000:3000 <yourname/projectname>
```