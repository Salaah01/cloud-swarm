/**
 * Checks the strength of the password return a list of weaknesses.
 * @param {String} password - password to test.
 */
export const check_password_strength = (password: string) => {
  const weaknesses = [];

  if (password.length < 6) {
    weaknesses.push("Must have more than than 5 characters.");
  }

  if (password.search(/[0-9]/) < 0) {
    weaknesses.push("Password must contain at least 1 number.");
  }

  if (password.search(/[A-z]/) < 0) {
    weaknesses.push("Password must contain at least 1 letter.");
  }

  return weaknesses;
};
