import React from "react";
import { shallow } from "enzyme";
import VideoFeed from "./VideoFeed";

describe("VideoFeed", () => {
  test("matches snapshot", () => {
    const wrapper = shallow(<VideoFeed />);
    expect(wrapper).toMatchSnapshot();
  });
});
