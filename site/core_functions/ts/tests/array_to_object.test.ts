/**Unittest for ``array_to_object``. */
import { array_to_object } from "../array_to_object";

describe("array_to_object", () => {
  it("should convert the array to an object.", () => {
    const result = array_to_object(
      [
        { id: 1, name: "name1", price: 100 },
        { id: 2, name: "name2", price: 200 },
      ],
      "id"
    );
    expect(result).toEqual({
      1: { id: 1, name: "name1", price: 100 },
      2: { id: 2, name: "name2", price: 200 },
    });
  });
});
