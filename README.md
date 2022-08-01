# SQLiDetector
Simple python script that helps you to detect SQL injection "Error based" by sending multiple requests with 9 payloads and check for 152 regex pattern for different databases.

![Header](https://github.com/eslam3kl/SQLiDetector/blob/main/SCREENSHOT.png)

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
And match for 152 error regex pattern for different databases. <br />
Source: https://github.com/sqlmapproject/sqlmap/blob/master/data/xml/errors.xml

## How it works? 
It's very simple, just organize your steps as following
1. Use your subdomain grabber script or tools. 
2. Use your links and URLs tools to greb all waybackurls. 
3. Pass the waybackurls file to the tool and it will test them. 
```
python3 sqli_detector.py <waybackurls_file.txt>
```

## How it tests the parameter? 
What's the difference between this tool and any other one? 
If we have a link like this one `https://example.com?file=aykalam&username=eslam3kl` so we have 2 parameters. It create 2 possible vulnerable URLs. 
1. It will work for every payload like the following 
```
https://example.com?file=123'&username=eslam3kl
https://example.com?file=aykalam&username=123'
```
2. It will send a request for every link and check if one of the patterns is exist using regex. 
3. For any vulnerable link, it will save it at seperate file for every process. 

## Upcoming updates
- [ ] Adding threads to increase the speed.
- [ ] Adding more paylaods.
- [ ] Enhace the output schema. 

If you want to contribute, Feel free to do that. You're welcomed :)

## Stay in touch <3 
[LinkedIn](https://www.linkedin.com/in/eslam3kl/) | [Blog](https://eslam3kl.medium.com/)  |  [Twitter](https://twitter.com/eslam3kll)
