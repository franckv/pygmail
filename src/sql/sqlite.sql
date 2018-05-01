--
-- Table message
--

CREATE TABLE IF NOT EXISTS message (
  id integer NOT NULL PRIMARY KEY,
  sender integer NULL,
  subject varchar(255) NULL,
  account integer NOT NULL,
  read boolean NOT NULL
);


-- --------------------------------------------------------

--
-- Table message_tag
--

CREATE TABLE IF NOT EXISTS message_tag (
  message_id integer NOT NULL,
  tag_id integer NOT NULL,
  PRIMARY KEY (message_id, tag_id)
);


-- --------------------------------------------------------

--
-- Table path
--

CREATE TABLE IF NOT EXISTS path (
  message_id integer NOT NULL,
  path varchar(255) NOT NULL,
  PRIMARY KEY (message_id)
);


-- --------------------------------------------------------

--
-- Table tag
--

CREATE TABLE IF NOT EXISTS tag (
  id integer NOT NULL PRIMARY KEY,
  name varchar(50) NOT NULL
);

-- --------------------------------------------------------

--
-- Table recipient
--

CREATE TABLE IF NOT EXISTS recipient (
  id integer NOT NULL PRIMARY KEY,
  first_name varchar(50) NULL,
  last_name varchar(50) NULL,
  display varchar(100) NULL,
  email varchar(50) NOT NULL
);

