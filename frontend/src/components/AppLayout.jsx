import { Outlet, useNavigation } from "react-router-dom";

import Header from "./Header";
import Loader from "./Loader";

function AppLayout() {
  const navigation = useNavigation();

  const isLoading = navigation.state === "loading";

  return (
    <div className="grid grid-rows-[auto_1fr] h-screen">
      {isLoading && <Loader />}
      <Header />
      <Outlet />
    </div>
  );
}

export default AppLayout;
