##  EvenSteven
is an open-source expense splitting app built using the Beeware framework. It offers a seamless and fair way for groups to divide expenses, ensuring that everyone pays their fair share without any hassle. With EvenSteven, you can easily create groups, add expenses, and split bills with friends, roommates, or colleagues. The app is designed to promote transparency and equity in financial transactions, making it the ideal solution for managing shared expenses in any setting. Join us in building a community-driven platform that simplifies the process of splitting bills and promotes financial harmony among friends.

## Installation

1. Create micromamba virtual environment:
    ``` bash
    micromambda env create -f .\environment.yml -y
    micromambda activate evensteven
    pip install -e .
    ```
2. Build for Android
    ``` bash
    briefcase build android
    ``` 