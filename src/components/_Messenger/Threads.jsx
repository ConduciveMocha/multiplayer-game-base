import React from "react";
import ThreadTabList from "./ThreadTabList";
const Threads = props => {
  const [activeTabList, setActiveTabList] = useState([]);
  const [activeTab, setActiveTab] = useState();

  return (
    <>
      <ThreadTabList
        activeThreads={activeTabList}
        onTabClick={th => setActiveTab(th)}
        onTabClose={th => {}}
      />
    </>
  );
};

export default ThreadTabs;
