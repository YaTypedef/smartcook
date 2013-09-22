#include "if/gen-cpp/Search.h"
#include "if/gen-cpp/search_types.h"

#include <thrift/protocol/TJSONProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/THttpServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TTransportUtils.h>

#include <memory>
#include <string>
#include <vector>

using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::server;
using namespace apache::thrift::transport;

using std::string;
using std::vector;


class SearchHandler : virtual public SearchIf {
public:
    void Find(vector<Recipe>& _return, const string& query) {
        Recipe r;
        r.title = "example";
        _return.push_back(r);
    }
};

int main() {
    boost::shared_ptr<SearchHandler> handler(new SearchHandler());
    boost::shared_ptr<SearchProcessor> processor(new SearchProcessor(handler));

    int port = 9090;
    boost::shared_ptr<TServerSocket> serverTransport(new TServerSocket(port));
    boost::shared_ptr<THttpServerTransportFactory> transportFactory(
            new THttpServerTransportFactory());
    boost::shared_ptr<TJSONProtocolFactory> protocolFactory( 
        new TJSONProtocolFactory());

    TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
    server.serve();

    return 0;
}
