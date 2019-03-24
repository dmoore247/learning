
set -x

export ENV=tk7

conda create --name ${ENV} -c conda-forge --file core-requirements.txt
conda activate ${ENV}

conda clean --all -y
SITE_PKGS=/root/miniconda3/envs/${ENV}/lib/python3.7/site-packages

find $SITE_PKGS -type f -exec touch {} \;

touch run
pytest lambda_test.py
find $SITE_PKGS -anewer run -and -type f >files.lst 
wc files.lst


rm -f  ${ENV}.zip
zip -r ${ENV}.zip $(cat files.lst)

rm -rf opt/*
cd opt
unzip ../${ENV}.zip
cd opt/root/miniconda3/envs/${ENV}/lib/python3.7/site-packages/
find . -type f -name '*.so' -exec strip {} \;
du -s -h .

rm -f    ~/${ENV}.1.zip
zip -r   ~/${ENV}.1.zip ./*
unzip -l ~/${ENV}.1.zip

aws s3 cp ~/${ENV}.1.zip s3://bin.takehome.power.io
