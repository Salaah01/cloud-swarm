import { BuildURL } from "../build_url";

describe("BuildURL", () => {
  const buildURL = new BuildURL();
  it("should append to the end of the top level domain.", () => {
    expect(buildURL.append("soaps")).toEqual("http://localhost/soaps");
  });
});
