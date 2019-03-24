
set -x

conda clean --all -y
SITE_PKGS=/root/miniconda3/envs/tk6/lib/python3.7/site-packages

find $SITE_PKGS -type f -exec touch {} \;

touch run
pytest lambda_test.py
find $SITE_PKGS -anewer run -and -type f >files.lst 
wc files.lst


rm -f  tk6.zip
zip -r tk6.zip $(cat files.lst)

rm -rf opt/*
cd opt
unzip ../tk6.zip
cd opt/root/miniconda3/envs/tk6/lib/python3.7/site-packages/
find . -type f -name '*.so' -exec strip {} \;
du -s -h .

rm -f  ~/tk6.1.zip
zip -r ~/tk6.1.zip ./*
unzip -l ~/tk6.1.zip

aws s3 cp ~/tk6.1.zip s3://bin.takehome.power.io
