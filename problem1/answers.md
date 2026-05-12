why is .env better than writing passwords in code?
usage of .env lets us make the code as generic as we want. this allows the application to run for different values but the codebase remains the same.
.env files are also ensures that they dont get pushed to repository allowing the passowrd to remain secure.
hence it makes the appliation stateless and portable.

why is treating the database as a seperate service useful?
this ensures that two different resources ie the application and the database service can independtly scale making the application and daatabase less dependent on each other and reduce coupling

why does docker make development and production similar?
A common source of bugs is "dependency drift"—where your laptop has libssl v1.1 but the production server was updated to v1.2.

Docker encapsulates the entire environment. The Dockerfile acts as a Source of Truth. If the Dockerfile says FROM postgres:16-alpine, then every developer on the team and every server in the cloud will be running that exact version. It eliminates the "it works on my machine" excuse because everyone is effectively using the same machine.
