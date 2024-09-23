# Discord Moderator Bot

## Description

This project was designed to streamline the automatic flagging of offending content and profiles to improve user safety from scams and spam.

Discord moderator bot built to protect against romance scams. Built with Python and Juypter Notebook.

[Here](https://drive.google.com/file/d/12S5HvyUz_vA4LiYZp7mXBhW8ZT7-2-nh/view?usp=sharing) is a video showing the functionality of the Bot.

## Table of Contents
  * [Background](#background) <br>
  * [Functionality](#functionality) <br>
    * [User Metadata Classifier](#user-metadata-classifier) <br>
    * [Automated Flagging](#automated-flagging) <br>
    * [Reporting](#reporting) <br>
  * [Installation](#installation) <br>
  * [Usage](#usage) <br>
  * [Credit](#credit) <br>
  * [Contributors](#contributors) <br>
  * [License](#license) <br>

## Background
Financial scams on dating platforms target victims by setting up desirable online profiles (e.g. catfishing) that are designed to con targets out of money. Cryptocurrency scams are a rising subset. In 2022 alone, 70,000 people in the U.S. reported being caught in a romance scam, with reported losses hitting a staggering $1.3 billion (1). 

Adults under 30 are the most prominent group on dating platforms and 6x more likely to be targets of dating apps scams than adults over 30 (2)(3). A second victim is the individual whose images are stolen; they can face harassment for being dragged into the abuse of others online.

Resolving this issue is a popular user demand (4).

## Functionality

### User Metadata Classifier

We developed a logistic regression classifier using a proxy dataset of real and inauthentic Instagram profiles which takes in user metadata and outputs a "suspicion score" which represents the likelihood that a profile is fraudulent, based on its metadata. This score is provided to moderators when a user's message is flagged, enabling rapid contextual analysis of the reported user's profile characteristics. 

Our classifier was developed using 1,500 data points derived from a proxy dataset of fake Instagram profiles. Following data processing and augmentation, it achieved an accuracy of 95.6% on the test set. The generation of synthetic fields related to our domain required assumptions about the underlying distributions, which could influence these results.

<img width="584" alt="User metadata classifier flowchart" src="https://github.com/user-attachments/assets/02ac8a2e-2a0d-474b-b2e2-9e9f16e8db9d"> <br>

Collected Fields: number of posts, description, contains external url <br>
Synthetic Fields: gender, time spent, response rate, first message sent

### Automated Flagging

All messages undergo automated analysis for concerning content, which is subsequently escalated to moderators for further review.
The matches of users of concern are automatically warned when a message suggests moving off-platform.

![AGV_vUc2brpe8-wuqxKXZH-ugkm4p3egD-EY2cLYw3X1jav-KXX3be2erMoLhVWSCiYzg_oKFIk-GrLlvMkmLGU4DhVL9kEIp9PuELdnmVyXxkCqHYsuXVoHqx8-](https://github.com/user-attachments/assets/535d6976-ebdf-410e-8c59-4e08870ab443)

### Reporting

<img width="500" alt="AGV_vUenXbwpJLmGxkNksiWdmVy0Yd1sXaKJXzZ0i7eQRDR9bM718gxRt6q8pXmeiltBYATw_1eMbN7LrIsJ0zQ3EVTI8pFHA4leMGW2TC8ehE6O33AcNElugFp4" src="https://github.com/user-attachments/assets/386bbc47-a3ae-4d7f-bade-35a0805ffbd1">

<img width="500" alt="AGV_vUcxw18yZ9NKlszyE6a34qWPyVtu_52agboUANjiFAH7gT-NCBCmLchEX4oAeGSWfHNmlwIIP3GRVNBdeJdtGrMUWYgjEB8-V6ThPSkRl4noqutjpJ4Ak6LG" src="https://github.com/user-attachments/assets/97a80802-5c71-41bf-aea9-8d81cb0c6919">

## Installation

N/A

## Usage

N/A

## Credit

[Original repository](https://github.com/AriGlenn/cs152bots-group-9)

Starter code provided by Stanford University CS152: https://github.com/stanfordio/cs152bots <br>

### References

1. Fletcher, Emma. "Romance scammers’ favorite lies exposed." Consumer Protection: Data Spotlight, Federal Trade Commission, 9 Feb. 2023, [FTC](https://www.ftc.gov/news-events/data-visualizations/data-spotlight/2023/02/romance-scammers-favorite-lies-exposed) <br>
2. Maltseva, Irina. “The 5 Latest Hinge Scams: How to Identify a Hinge Scammer.” Aura, 24 July 2023, [Aura](www.aura.com/learn/hinge-scammers.) <br>
3. McClain, Colleen, and Gelles-Watnick, Risa. “The Who, Where and Why of Online Dating in the U.S.” Pew Research Center, Pew Research Center, 2 Feb. 2023, [Pew](www.pewresearch.org/internet/2023/02/02/the-who-where-and-why-of-online-dating-in-the-u-s/#:~:text=Some%20dating%20platforms%20are%20especially,and%202%25%20have%20used%20Hinge.) <br>
4. Dixon, Stacy Jo. "Responsibilities of social media companies regarding catfishing according to adults in the United States as of January 2022". Morning Consult, Statista, 27 Jan. 2022),  [Statista](https://www.statista.com/statistics/1295015/us-adults-social-media-companies-catfishing-responsibilities-by-age-group/) <br>

## Contributors
Ari Glenn <br>
[Github](https://github.com/AriGlenn)

Larsen Weigle <br>
[Github](https://github.com/larsenweigle)

Giancarlo Ricci <br>
[Github](https://github.com/giancarloricci)

Gabrielle Belanger <br>
[Github](https://github.com/gcbel)

## License

[MIT License](https://opensource.org/license/mit)
