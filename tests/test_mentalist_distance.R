test_that("Test ham_distance 0", {
  X <- data.frame(c(0,0))
  expect_equal(ham_distance(X), matrix(c(0,0,0,0), nrow=2, ncol=2))
})

test_that("Test ham_distance 1", {
  X <- data.frame(c(0,1))
  expect_equal(ham_distance(X), matrix(c(0,1,1,0), nrow=2, ncol=2))
})