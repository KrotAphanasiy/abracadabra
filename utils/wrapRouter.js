const wrapRouter = (func) => async (req, res, next) => {
  try {
    return await func(req, res, next);
  }
  catch (err) {
    return next(err);
  }
};

module.exports = wrapRouter;
