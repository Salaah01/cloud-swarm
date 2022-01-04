import { check_password_strength } from "../check_password_strength";

describe("check_password_strength", () => {
  it("should fail the password test (less than 6 chars and no numbers).", () => {
    const test = check_password_strength("abc");
    expect(test).toEqual([
      "Must have more than than 5 characters.",
      "Password must contain at least 1 number.",
    ]);
  });

  it("should fail the password test (no letters).", () => {
    const test = check_password_strength("123456789");
    expect(test).toEqual(["Password must contain at least 1 letter."]);
  });

  it("should pass to password test.", () => {
    const test = check_password_strength("ef337dfd@skd1h&h2hasd");
    expect(test).toEqual([]);
  });
});
