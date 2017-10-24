import random
import cgitb
import cgi
cgitb.enable()
form=cgi.FieldStorage()


A=random.random()
if A<0.3:
    template ="""
<html>
<head>
   <title> sound </title>
   
  
<bgsound src="/aki-nasi.mp3" loop="infinite">
</head>
<body>
<p>音声を再生するには、audioタグをサポートしたブラウザが必要です。</p>

</body>

</html>
"""
    

elif 0.3<=A<=0.6:
    template ="""
<html>
<head>
 <meta charset="shift-jis">
 <body bgcolor="fff99">
   <title> sound </title>

   <p>sound</p>
   
   
   <bgsound src="/1F-aki.mp3" loop="infinite">

 
</head>   
   

</body>
</body>
</html>
"""
elif 0.6<A:
    template ="""
<html>
<head>
 <meta charset="shift-jis">

   <title> sound </title>

   <p>sound</p>
   
   
   <bgsound src="/2F-aki.mp3" loop="infinite">

 
</head>   
   

</body>
</body>
</html>
"""    
    



print("Content-type: text/html\n")
print(template)

