import React from "react";
import { shallow } from "enzyme";
import ProcessedBatches from "./ProcessedBatches";

describe("ProcessedBatches", () => {
  test("matches snapshot", () => {
    const wrapper = shallow(<ProcessedBatches />);
    expect(wrapper).toMatchSnapshot();
  });
});
