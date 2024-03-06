//
// Created by Laky64 on 30/08/2023.
//

#include "shell_reader.hpp"

#ifdef BOOST_ENABLED
namespace ntgcalls {
    ShellReader::ShellReader(const std::string &command, const int64_t bufferSize, const bool noLatency): BaseReader(bufferSize, noLatency) {
        try {
            shellProcess = bp::child(command, bp::std_out > stdOut, bp::std_in < stdIn);
        } catch (std::runtime_error &e) {
            throw ShellError(e.what());
        }
    }

    ShellReader::~ShellReader() {
        close();
        stdOut.clear();
        stdIn.clear();
    }

    wrtc::binary ShellReader::readInternal(const int64_t size) {
        if (!stdOut || stdOut.eof() || stdOut.fail() || !stdOut.is_open()) {
            throw EOFError("Reached end of the stream");
        }
        auto file_data = std::make_shared<uint8_t[]>(size);
        stdOut.read(reinterpret_cast<char*>(file_data.get()), size);
        return file_data;
    }

    void ShellReader::close() {
        BaseReader::close();
        if (stdOut) {
            stdOut.close();
            if (auto pipe = stdOut.pipe(); pipe.is_open()){
                pipe.close();
            }
        }
        if (stdIn) {
            stdIn.close();
            if (auto pipe = stdIn.pipe(); pipe.is_open()){
                pipe.close();
            }
        }
        if (shellProcess) {
            shellProcess.terminate();
            shellProcess.wait();
            shellProcess.detach();
        }
    }
} // ntgcalls
#endif
