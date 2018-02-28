## Calculate of Nagelkerke R2.
## Do logistic regression, output summary statistics and also several correlation metrics.
## Read data with header from stdin, and output results to stdout.
## The first column is binary dependent variable.
## From second to last, are independent variables.

RsqGLM <- function(obs = NULL, pred = NULL, model = NULL) {
  # version 1.2 (3 Jan 2015)

  model.provided <- ifelse(is.null(model), FALSE, TRUE)

  if (model.provided) {
    if (!("glm" %in% class(model))) stop ("'model' must be of class 'glm'.")
    if (!is.null(pred)) message("Argument 'pred' ignored in favour of 'model'.")
    if (!is.null(obs)) message("Argument 'obs' ignored in favour of 'model'.")
    obs <- model$y
    pred <- model$fitted.values

  } else { # if model not provided
    if (is.null(obs) | is.null(pred)) stop ("You must provide either 'obs' and 'pred', or a 'model' object of class 'glm'")
    if (length(obs) != length(pred)) stop ("'obs' and 'pred' must be of the same length (and in the same order).")
    if (!(obs %in% c(0, 1)) | pred < 0 | pred > 1) stop ("Sorry, 'obs' and 'pred' options currently only implemented for binomial GLMs (binary response variable with values 0 or 1) with logit link.")
    logit <- log(pred / (1 - pred))
    model <- glm(obs ~ logit, family = "binomial")
  }

  null.mod <- glm(obs ~ 1, family = family(model))
  loglike.M <- as.numeric(logLik(model))
  loglike.0 <- as.numeric(logLik(null.mod))
  N <- length(obs)

  # based on Nagelkerke 1991:
  CoxSnell <- 1 - exp(-(2 / N) * (loglike.M - loglike.0))
  Nagelkerke <- CoxSnell / (1 - exp((2 * N ^ (-1)) * loglike.0))

  # based on Allison 2014:
  McFadden <- 1 - (loglike.M / loglike.0)
  Tjur <- mean(pred[obs == 1]) - mean(pred[obs == 0])
  sqPearson <- cor(obs, pred) ^ 2

  return(list(CoxSnellR2 = CoxSnell, NagelkerkeR2 = Nagelkerke, McFaddenR2 = McFadden, TjurR2 = Tjur, sqPearsonR2 = sqPearson))
}

# clotting <- data.frame(
#   u = c(0,0,0,0,0,1,1,1,1),
#   lot1 = c(118,58,42,35,27,25,21,19,18),
#   lot2 = c(69,35,26,21,18,16,13,12,12))

#dd = read.table("test.txt",header = T)
dd = read.table(file("stdin"),header = T)
# https://stackoverflow.com/questions/4951442/formula-with-dynamic-number-of-variables
# auto convert the colnames as formula.
form = sub('\\+','~',paste(colnames(dd), collapse = '+'))

print("FORMULA:")
print(form)

lr = glm(as.formula(form),data = dd, family = binomial(link="logit"))
summary(lr)
r2 = RsqGLM(model=lr)
str(r2, comp.str = "")
