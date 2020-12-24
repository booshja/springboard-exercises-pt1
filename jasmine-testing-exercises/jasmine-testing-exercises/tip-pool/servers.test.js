describe("Servers test (with setup and tear-down)", function () {
  beforeEach(function () {
    // initialization logic
    serverNameInput.value = "Alice";
  });

  it("should add a new server to allServers on submitServerInfo()", function () {
    submitServerInfo();

    expect(Object.keys(allServers).length).toEqual(1);
    expect(allServers["server" + serverId].serverName).toEqual("Alice");
  });

  it("shouldn't add a new server with no input", function () {
    serverNameInput.value = "";
    submitServerInfo();
    expect(Object.keys(allServers).length).toEqual(0);
  });

  it("should update server table on updateServerTable()", function () {
    submitServerInfo();
    let tdList = document.serverTbody.querySelectorAll(
      "#serverTable tbody tr td"
    );

    expect(tdList.length).toEqual(3);
    expect(tdList[0].innerText).toEqual("Alice");
    expect(tdList[1].innerText).toEqual("$0.00");
  });

  afterEach(function () {
    allServers = {};
    serverId = 0;
    serverTbody.innerHTML = "";
  });
});
