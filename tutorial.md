In this tutorial, we will be building an app which exposes classifiers through a
web application, with Gramex. By the end of this tutorial, we will have covered:

1. How to expose data as a REST API through
   [formhandler](https://gramener.com/gramex/guide/formhandler)
2. How to train scikit-learn classifiers on uploaded datasets through
   [functionhandler](https://gramener.com/gramex/guide/functionhandler)
3. How to visualize certain elements of the trained model through JS and Vega

By the end, the app should look something like:
![](assets/decisiontree.png)

You can also play with a live version of the app [here](https://9018.gramex.gramener.co).


## FormHandler: Exposing Data Through a REST API
