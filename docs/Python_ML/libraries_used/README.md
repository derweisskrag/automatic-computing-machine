# Libraries used in the `Tomodachi`

## Overview:

```
pandas
numpy
python-dotenv
seaborn
plotly
graphviz
scikit-learn
scipy
tensorflow
tensorflow-decision-forests
tensorflow-estimator
xgboost
lightgbm
catboost
mlxtend
optuna
shap
```

As we go with SPRINTs, we add more and more libraries to experiment with and 
use the best one for our project. For example, we can create a model using `DecisionTreeClassifier` from
`sklearn` and then apply `XGBoost` library to implement gradient boosting for our features (we choose `Power Output`, `Time` - hours, days, weeks, etc) and 
we want to target some variable that we want to predict. So, it can be

- y is the Wind Power
- X are wind_speed, wind_gust, time-related variables (based on features that affect our project the most)

Once ready, we just apply the `Gradient Boosting` and ***train*** our model. The **training** means that each new model will learn from the previous model using the
parameter called `residuals` which means: ***error*** and we improve on the model by decreasing the error. To check out the error, we usually use

| > sklearn.metrics:

- root_mean_squared_error
- mean_absolute_error
- r2_score

Not always, but *ROC AUC* is also applicable whenever we got ***classifier model***. 

### An example

The model predicts if the input points to the cat. We see: boolean, or we can assume

```rs
struct Input {
    data: Vec<i32>
}

struct Output {
    response: u8
}
```

In this situation, we see Classifier model. It classifies if the animal given is a cat or not. 
Meaning you can go and compute the ***ROC AUC*** score. 

## Basic libraries

So far, we used the following:

- pandas
- numpy
- seaborn
- plotly

These 4 are the most fundamental libraries. They allow us to work with data and calculate the statistics. The last two
are the modern version of `matplotlib.pyplot` which creates visualization. In addition to them, we got `graphviz`. This 
is a powerful library that uses `graphviz` engine to create visualization of the decision tree, for example. The non-linear model
is usually represented using graphs. So, this particular engine helps to draw the model's graph. 

Please, notice that plotly is a good library for interactive visualization. Unlike seaborn, it allows you to study the graph interactively.
What does it mean? It means that you can skew, zoom, and sometimes change the weights. 

A basic example of the interactive graph using `matplotlib.pyploy` and `ipywidgets` and the example was

```py
def f(m, b):
    plt.figure(2)
    x = np.linspace(-10, 10, num=1000)
    plt.grid()
    plt.plot(x, m*x + b, label="y = mx + b")
    plt.scatter(df["x"], df["y"], color="red", label="Data")
    plt.title("Linear Regression Model")
    plt.xlim(-1, 7)
    plt.ylim(-1, 3)
    plt.show()

interactive_plot = interactive(f, m=(-2.0, 2.0), b=(-3, 3, 0.5))
output = interactive_plot.children[-1]
output.layout.height = '400px'
interactive_plot
```

Please, refer to "./playground/sklearn_models/linear_regression.ipynb" for more insights.

## Machine Learning

Here, we use much more. Based on the `lab 4` and `lab 5`, we learned that:

- First, we preprocess data (checking types, values, and missing values)
- Second, we split the data into actual and training
- Third, we balance the data (using `imbalanced_learn` library)
- Fourth, we use the Scaler (Depending on what data we got we use StandardScaler or others)
- Fifth, we create the right model
- Sixth, we apply the machine learning pattern to minimize error and train the model (e. g., Gradient Boosting)

Once done, we prepare the model for deployment.

So, what kind of libraries we use here? The answer is

- scipy
- scikit-learn
- tensorflow
- tensorflow-decision-forests
- tensorflow-estimator
- xgboost
- lightgbm
- catboost

## Deployment

Here, I have nothing to say, but we will use

- FastAPI
- mlxtend
- optuna
- shap

Primarily, I want to use Zig for Python/ML bridge to Rust. Once done, Rust can use gRCP for Kotlin, and Kotlin is the main back-end. 
We dockerize all the microservices. As for front-end, we gonna use NextJS and possibly: Wasm + Nuxt if we see advantages. 

In the simplest case, 

Decision Tree - model
Gradient Boosting - the training
streamlit - dashboard
server=Flask

This is the simplest setup we can do if we are short on time. The Flask is easily dockerized for deployment. We already use Lua for scripting,
which means we would add more scripts for more automation and update pipeline accordingly. We also create pipeline for back-up when emergency happens.