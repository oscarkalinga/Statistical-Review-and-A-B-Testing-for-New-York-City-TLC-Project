# Statistical Review and A/B Testing for New York City TLC Project

# Project Overview
The goal of this project was to apply descriptive statistics and hypothesis testing in Python. The goal of this A/B test is to sample data and analyze whether there is a relationship between payment type and fare amount. For example: discover if customers who use credit cards pay higher fare amounts than customers who use cash. The Automatidata team ran an A/B test to analyze the relationship between credit card payments and total fare amounts. The key business insight is that encouraging customers to pay with credit cards will likely generate more revenue for taxi drivers. 


# Problem Statement
Taxi cab drivers receive varying amounts of tips. While examining the relationship between total fare amount and payment type, this project seeks to discover if customers who pay with credit cards tend to pay a larger total fare amount than customers who pay in cash. 

# Business Understanding
Automatidata works with its clients to transform their unused and stored data into useful solutions, such as performance dashboards, customer-facing tools, strategic business insights, and more. They specialize in identifying a client’s business needs and utilizing their data to meet those business needs. 

Automatidata is consulting for the New York City Taxi and Limousine Commission (TLC). New York City TLC is an agency responsible for licensing and regulating New York City's taxi cabs and for-hire vehicles. The agency has partnered with Automatidata to develop a regression model that helps estimate taxi fares before the ride, based on data that TLC has gathered. 

The TLC data comes from over 200,000 taxi and limousine licensees, making approximately one million combined trips per day. 

> Note: This project's dataset was created for pedagogical purposes and may not be indicative of New York City taxi cab riders' behaviour.

## The members of Automatidata and the New York City TLC 
Automatidata Team Members
<ul>
  <li>Udo Bankole, Director of Data Analysis</li>
  <li>Deshawn Washington, Data Analysis Manager</li>
  <li>Luana Rodriquez, Senior Data Analyst</li>
  <li>Uli King, Senior Project Manager</li>
</ul>

New York City TLC Team Members
<ul>
  <li>Juliana Soto, Finance and Administration Department Head</li>
  <li>Titus Nelson, Operations Manager</li>
</ul>

> Note: The story, all names, characters, and incidents portrayed in this project are fictitious. No identification with actual persons (living or deceased) is intended or should be inferred. The data shared in this project has been altered for pedagogical purposes.

# Data Understanding
The user data came from Otomatidata via Google. The data consisted of approximately 22k unique users and 17 features. The features included information on ID, trip distances, fare amount, payment type, and toll amount. The bar chart below shows the breakdown of users by payment type. Users with Credit cards accounted for about 67.25%, Cash users 32.01%

![image](https://github.com/oscarkalinga/Statistical-Review-and-A-B-Testing-for-New-York-City-TLC-Project/assets/73540285/cf79eb25-cdd8-44a2-ac71-9bc8f729093d)

# Steps conducted in the A/B test
<ol>
  <li>Collected sample data from an experiment in which customers are randomly selected and divided into two groups:</li>
  <ul>
    <li>Customers who are required to pay with a credit card.</li>
    <li>Customers who are required to pay with cash. This enables us to draw causal conclusions about how payment method affects fare amount.</li>
  </ul>
  <li>Computed descriptive statistics to better understand the average total fare amount for each payment method available to the customer.</li>
  <li>Conducted a two-sample t-test to determine if there is a statistically significant difference in average total fare between customers who use credit cards and customers who use cash. </li>
</ol>

# A/B test results
There is a statistically significant difference in the average total fare between customers who use credit cards and customers who use cash. Customers who used credit cards showed a higher total amount compared to cash

# Recommendations
The Automatidata data team recommends that the New York City TLC encourages customers to pay with credit cards and create strategies to promote credit card payments. For example, the New York City TLC can install signs that read “Credit card payments are preferred” in their cabs, and implement a protocol that requires cab drivers to verbally inform customers that credit card payments are preferred. 
