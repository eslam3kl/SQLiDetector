# SQLiDetector
Simple python script that helps you to detect SQL injection "Error based" by sending multiple requests with 9 payloads and check for 152 regex pattern for different databases.

## Description
The main idea for the tool is scanning for Error Based SQL Injection by using different paylaods like
```
' 
"
'' Double Singel quote
'" Single quote + Double qoute
"' Double quote + single quote
:) 
"" Double Double quote
\
[]
```
And match for 152 error regex pattern for different databases. 
