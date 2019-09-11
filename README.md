joker-superuser
===============

### Miscellaneous 

Get resources with SVN:

    svn export https://github.com/frozflame/joker-superuser/trunk/resources sus-resources
    
Get resources with curl and GNU tar:
   
    curl -L "https://github.com/frozflame/joker-superuser/archive/master.tar.gz" | tar xz joker-superuser-master/resources --strip-components 1 --transform s/resources/sus-resources/ 
    
Get resources with curl and BSD tar:

    curl -L "https://github.com/frozflame/joker-superuser/archive/master.tar.gz" | tar -xz --strip-components 1 -s /resources/sus-resources/ joker-superuser-master/resources 
 
