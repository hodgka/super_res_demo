echo "Prepare DIV2K X4 datasets..."

DATA_DIR='/u/big/workspace_hodgkinsona/super_res_demo/ml_modules/datasets'
SCRIPT_DIR="${DATA_DIR}/scripts"

cd $DATA_DIR
mkdir -p DIV2K
cd DIV2K

#### Step 1
echo "Step 1: Download the datasets: [DIV2K_train_HR] and [DIV2K_train_LR_bicubic_X4]..."
# GT
FOLDER=DIV2K_train_HR
FILE=DIV2K_train_HR.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/$FILE
    fi
    unzip $FILE
fi

# LR
FOLDER=DIV2K_train_LR_bicubic
FILE=DIV2K_train_LR_bicubic_X4.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X4.zip
    fi
    unzip $FILE
fi
# LR
FOLDER=DIV2K_train_LR_bicubic/X3
FILE=DIV2K_train_LR_bicubic_X3.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X3.zip
    fi
    unzip $FILE
fi

# LR
FOLDER=DIV2K_train_LR_bicubic/X2
FILE=DIV2K_train_LR_bicubic_X2.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X2.zip
    fi
    unzip $FILE
fi

#### Step 1
echo "Step 2: Download the datasets: [DIV2K_valid_HR] and [DIV2K_valid_LR_bicubic_X4]..."
# GT
FOLDER=DIV2K_valid_HR
FILE=DIV2K_valid_HR.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/$FILE
    fi
    unzip $FILE
fi

# LR
FOLDER=DIV2K_valid_LR_bicubic
FILE=DIV2K_valid_LR_bicubic_X4.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X4.zip
    fi
    unzip $FILE
fi
# LR
FOLDER=DIV2K_valid_LR_bicubic/X3
FILE=DIV2K_valid_LR_bicubic_X3.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X3.zip
    fi
    unzip $FILE
fi

# LR
FOLDER=DIV2K_valid_LR_bicubic/X2
FILE=DIV2K_valid_LR_bicubic_X2.zip
if [ ! -d "$FOLDER" ]; then
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X2.zip
    fi
    unzip $FILE
fi




#### Step 3
echo "Step 3: Rename the LR images..."
cd $SCRIPT_DIR
python3 rename.py

#### Step 4
echo "Step 4: Crop to sub-images..."
python3 extract_subimages.py

#### Step 5
echo "Step5: Create LMDB files..."
python3 create_lmdb.py
