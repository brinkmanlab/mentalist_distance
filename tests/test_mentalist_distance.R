test_that("Test ham_distance", {
  X <- data.frame(c(0), c(0))
  expect_equal(ham_distance(X), as.matrix(0))
})